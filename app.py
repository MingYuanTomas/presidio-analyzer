from flask import Flask, request, jsonify
from presidio_analyzer import AnalyzerEngine
from presidio_analyzer.nlp_engine import NlpEngineProvider
import stanza

app = Flask(__name__)

# 初始化分析器
def init_analyzer():
    print("初始化中文分析器...")
    stanza.download('zh')

    configuration = {
        "nlp_engine_name": "stanza",
        "models": [{"lang_code": "zh", "model_name": "zh"}]
    }

    provider = NlpEngineProvider(nlp_configuration=configuration)
    nlp_engine = provider.create_engine()
    analyzer = AnalyzerEngine(nlp_engine=nlp_engine, supported_languages=["zh"])

    print("分析器初始化完成")
    return analyzer

analyzer = init_analyzer()

@app.route('/health', methods=['GET'])
def health_check():
    """健康检查端点"""
    return jsonify({"status": "healthy", "service": "presidio-chinese-analyzer"})

@app.route('/analyze', methods=['POST'])
def analyze_text():
    """分析文本端点"""
    try:
        data = request.get_json()

        if not data or 'text' not in data:
            return jsonify({"error": "缺少 text 字段"}), 400

        text = data['text']
        language = data.get('language', 'zh')

        # 执行分析
        results = analyzer.analyze(text=text, language=language)

        # 格式化结果
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
            "original_text": text,
            "results": formatted_results
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
