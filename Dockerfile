FROM registry.cn-hangzhou.aliyuncs.com/mingyuan_cloud_native/presidio-analyzer:latest

WORKDIR /app


# 复制依赖文件


# 复制应用代码
COPY . .

# 预下载模型

# 创建非root用户
RUN useradd --create-home --shell /bin/bash app && \
    chown -R app:app /app
USER app

EXPOSE 5000

CMD ["python", "app.py"]
