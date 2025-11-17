FROM python:3.11-slim

WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# 使用国内镜像源
RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
RUN pip config set global.trusted-host pypi.tuna.tsinghua.edu.cn

# 先单独安装 spacy 并强制使用二进制
RUN pip install --no-cache-dir --only-binary=all spacy>=3.0.0

# 然后安装其他依赖
COPY requirements.txt .
RUN pip install --no-cache-dir --only-binary=all -r requirements.txt

COPY . .

EXPOSE 8000
CMD ["python", "app.py"]
