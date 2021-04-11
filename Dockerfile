# 任意のイメージを取得
FROM python:3.10-rc-slim-buster

RUN pip install python-dotenv requests

WORKDIR /app

COPY app /app
COPY start.sh /start.sh

RUN chmod 755 /start.sh

RUN python --version

CMD [ "/start.sh" ]
