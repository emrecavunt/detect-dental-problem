FROM python:3.6-slim-stretch
MAINTAINER Emre Cavunt <emre.cavunt@gmail.com>


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

RUN mkdir /opt/detect-dental-problem/
COPY app /opt/detect-dental-problem/

RUN ls

RUN echo "------"

RUN ls /opt

RUN echo "------"


RUN ls /opt/detect_dental_problem


RUN echo "------"


RUN python opt/detect-dental-problem/

EXPOSE 8080

CMD ["python", "opt/detect_dental_problem/server.py", "serve"]
