FROM registry.cn-hangzhou.aliyuncs.com/mingyuan_cloud_native/presidio-analyzer:latest

WORKDIR /app


# 复制依赖文件


# 复制应用代码
COPY . .



EXPOSE 5000
ENV STANZA_DOWNLOAD_METHOD=none
ENV STANZA_RESOURCES_DEVICE=cpu
CMD ["python", "app.py"]
