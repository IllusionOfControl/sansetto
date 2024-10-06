FROM python:3.11-slim

ARG MODEL_URL=https://huggingface.co/oovm/deep-danbooru/resolve/main/models/deepdanbooru-2021.onnx?download=true
ARG LABELS_URL=https://huggingface.co/oovm/deep-danbooru/resolve/main/models/deepdanbooru-2021.tags?download=true

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN curl -L --silent $MODEL_URL -o ./models/deepdanbooru-2021.onnx; \
    curl -L --silent $LABELS_URL -o ./models/deepdanbooru-2021.tags

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0"]