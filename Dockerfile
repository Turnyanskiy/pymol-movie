FROM ubuntu:latest
ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update && apt-get install -y software-properties-common gcc && \
    add-apt-repository -y ppa:deadsnakes/ppa

RUN apt-get update && apt-get install -y python3.8 python3-distutils python3-pip python3-apt

RUN apt-get install -y pymol
RUN pip3 install pyyaml

COPY . .
ENTRYPOINT ["python3", "./src/__main__.py"]
