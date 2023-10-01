FROM python:3.11-bullseye

WORKDIR /app
COPY . /app

RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir -y gunicorn

ENV TZ=Asia/Seoul
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN apt-get update && apt-get install -y supervisor

#unit test
ENV API_SERVER_PROFILE=test
RUN pytest || exit 1
RUN rm -f ./test

#production
ENV API_SERVER_PROFILE=production
ADD supervisord.conf /etc/supervisor/conf.d/

ENTRYPOINT ["/usr/bin/supervisord"]