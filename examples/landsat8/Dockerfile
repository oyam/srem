FROM ubuntu:18.04

RUN \
  apt -y update --fix-missing && \
  apt -y install software-properties-common && \
  apt -y update && \
  apt -y upgrade && \
  apt -y install git gdal-bin libgdal-dev python3-gdal python3-pip libsm6 libxext6 libxrender-dev && \
  rm -rf /var/lib/apt/lists/*

COPY . /workspace

RUN \
  cd /workspace/src/l8_angles && \
  make && \
  mv l8_angles /usr/local/bin && \
  cd /workspace && \
  pip3 install --no-cache-dir -r requirements.txt

WORKDIR /workspace
