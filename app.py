from flask import Flask, request, jsonify
import stanza
from presidio_analyzer import AnalyzerEngine
from presidio_analyzer.nlp_engine import NlpEngineProvider
import logging
import os

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

class ChineseAnalyzerService:
    def __init__(self):
        self.analyzer = None
        self.initialized = False
        
    def initialize_without_download(self):
        """初始化分析器，不下载模型"""
        try:
            logger.info("尝试初始化中文分析器（不下载模型）...")
            
            # 直接尝试加载模型，不下载
            configuration = {
                "nlp_engine_name": "stanza",
                "models": [{"lang_code": "zh", "model_name": "zh"}]
            }
            
            provider = NlpEngineProvider(nlp_configuration=configuration)
            nlp_engine = provider.create_engine()
            
            self.analyzer = AnalyzerEngine(
                nlp_engine=nlp_engine, 
                supported_languages=["zh"]
            )
            
            # 测试一下是否工作
            test_result = self.analyzer.analyze(text="测试", language="zh")
            logger.info("分析器测试成功")
            
            self.initialized = True
            logger.info("✓ 中文分析器初始化完成")
            return True
            
        except Exception as e:
            logger.error(f"初始化失败: {e}")
            logger.info("模型可能不存在，需要先下载")
            return False

# 创建服务实例
service = ChineseAnalyzerService()

@app.route('/', methods=['GET'])
def home():
    return jsonify({
        "message": "Presidio 中文分析器服务",
        "status": "running" if service.initialized else "model_missing",
        "analyzer_initialized": service.initialized
    })

@app.route('/health', methods=['GET'])
def health_check():
    status = "healthy" if service.initialized else "model_missing"
    return jsonify({
        "status": status, 
        "analyzer_ready": service.initialized
    })

@app.route('/analyze', methods=['POST'])
def analyze_text():
    if not service.initialized:
        return jsonify({
            "error": "分析器未初始化",
            "message": "需要先下载中文模型，请检查网络连接或手动安装模型"
        }), 503
        
    try:
        data = request.get_json()
        text = data.get('text', '')
        
        if not text:
            return jsonify({"error": "text 字段不能为空"}), 400
        
        results = service.analyzer.analyze(text=text, language="zh")
        
        formatted_results = []
        for result in results:
            formatted_results.append({
                "entity_type": result.entity_type,
                "text": text[result.start:result.end],
                "start": result.start,
                "end": result.end,
                "score": round(result.score, 4)
            })
        
        return jsonify({
            "success": True,
            "original_text": text,
            "results": formatted_results,
            "entities_count": len(formatted_results)
        })
        
    except Exception as e:
        logger.error(f"分析过程中出错: {e}")
        return jsonify({"error": str(e)}), 500

# 不自动初始化，等待手动触发
@app.route('/init', methods=['POST'])
def init_analyzer():
    """手动初始化分析器"""
    if service.initialized:
        return jsonify({"message": "分析器已初始化"})
    
    success = service.initialize_without_download()
    if success:
        return jsonify({"message": "分析器初始化成功"})
    else:
        return jsonify({"error": "分析器初始化失败，需要下载模型"}), 500

if __name__ == '__main__':
    logger.info("启动 Flask 应用...")
    # 不自动初始化分析器
    app.run(host='0.0.0.0', port=5000, debug=False)
