FROM python:3.14-slim
RUN pip install --no-cache-dir Pillow flask
COPY webapp.py /app/webapp.py
WORKDIR /app
EXPOSE 5000
CMD ["python", "webapp.py"]
