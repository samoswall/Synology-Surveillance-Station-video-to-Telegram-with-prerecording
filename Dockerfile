# syntax=docker/dockerfile:1

FROM python:alpine
RUN python -m venv /opt/venv

ENV PATH="/opt/venv/bin:$PATH" PIP_NO_CACHE_DIR=off

COPY requirements.txt .

RUN pip3 install --upgrade pip setuptools-rust wheel

RUN pip3 install -r requirements.txt && rm -rf /root/.cache /root/.cargo

EXPOSE 7878:7878
ENV TG_CHAT_ID=123456
ENV TG_TOKEN='1234567890:AAAAAAbbbbbbCCCC1234567890abcdefgh'
ENV SYNO_IP='192.168.1.1'
ENV SYNO_PORT=5000
ENV SYNO_LOGIN=login
ENV SYNO_PASS=password

WORKDIR /app

COPY ["Python code/main.py", "/app/"]

CMD ["gunicorn", "--bind", ":7878", "--workers", "1", "main:app"]