FROM ubuntu:18.04

RUN \
  apt -y update --fix-missing && \
  apt -y install software-properties-common && \
  apt -y update && \
  apt -y upgrade && \
  apt -y install git gdal-bin libgdal-dev python3-gdal python3-pip libsm6 libxext6 libxrender-dev && \
  rm -rf /var/lib/apt/lists/*

WORKDIR /workspace
COPY requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . /workspace
