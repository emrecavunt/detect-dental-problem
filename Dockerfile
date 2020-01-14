FROM python:3.6-slim-stretch
MAINTAINER Emre Cavunt <emre.cavunt@gmail.com>

RUN mkdir /opt/detect_dental_problem/
WORKDIR /opt/detect_dental_problem/

RUN apt-get update
RUN apt-get install --yes software-properties-common
RUN apt-add-repository contrib
RUN apt-get update

RUN apt-get install --yes \
    # python \
    python3-dev gcc \
    #python-dev \
    python-pip \
    build-essential \
    git \
    bash \
    strace \
  #&& pip install virtualenv \
  # && pip install 'pillow<7.0.0' \
  && rm -rf /var/cache/apk/* \
  && apt-get clean

ADD requirements.txt requirements.txt
RUN pip --no-cache-dir install -r requirements.txt

COPY dist/detect_dental_problem /opt/detect_dental_problem/

RUN python app/server.py

EXPOSE 8080

CMD ["python", "app/server.py", "serve"]
