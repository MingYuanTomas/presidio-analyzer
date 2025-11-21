FROM registry.cn-hangzhou.aliyuncs.com/mingyuan_cloud_native/python:3.9-slim

# 设置工作目录
WORKDIR /app

# 设置环境变量
ENV PYTHONUNBUFFERED=1

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# 先安装基础依赖（不包含 presidio-analyzer）
RUN pip install --no-cache-dir \
    stanza==1.8.0 \
    flask==2.3.3 \
    gunicorn==21.2.0

# 然后安装 presidio-analyzer
RUN pip install --no-cache-dir presidio-analyzer==2.2.30
