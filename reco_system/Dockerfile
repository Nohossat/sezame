FROM python:3.8

RUN mkdir -p /app/reco_system
WORKDIR /app
COPY . ./reco_system

RUN pip install -r ./reco_system/requirements.txt

EXPOSE 5000

ENV FLASK_APP reco_system
ENV FLASK_ENV development
ENV FLASK_RUN_HOST=0.0.0.0

CMD ["flask", "run"]