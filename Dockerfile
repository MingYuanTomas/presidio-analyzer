FROM registry.cn-hangzhou.aliyuncs.com/mingyuan_cloud_native/python:3.9-slim

# 设置工作目录
WORKDIR /app

# 设置环境变量
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# 复制依赖文件
COPY requirements.txt .

# 安装 Python 依赖
RUN pip install --no-cache-dir -r requirements.txt

# 预下载 Stanza 中文模型（在复制应用代码之前）
RUN python -c "\
from presidio_analyzer.nlp_engine import StanzaNlpEngine; \
nlp_engine = StanzaNlpEngine(models={'zh': 'zh'}); \
print('Stanza Chinese model downloaded successfully')\
"
