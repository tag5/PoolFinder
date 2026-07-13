FROM python:3.14-slim
RUN useradd -m appuser
USER appuser
RUN pip install --no-cache-dir Pillow requests
COPY scrapper.py /app/scrapper.py
WORKDIR /app
CMD ["python", "scrapper.py"]
