FROM python:3.11-bullseye

WORKDIR /app
COPY . /app

RUN mkdir data
RUN mkdir ./data/img
RUN mkdir ./data/tmp
RUN pip install --no-cache-dir -r requirements.txt
RUN yes | pip install gunicorn
ENV TZ=Asia/Seoul
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN apt-get update && apt-get install -y supervisor

#unit test
ENV API_SERVER_PROFILE=test
RUN python -m pytest . || exit 1
RUN rm -rf ./test
RUN rm -rf .pytest_cache

#production
ENV API_SERVER_PROFILE=production

ENTRYPOINT ["/usr/bin/supervisord", "-c", "./supervisord.conf"]