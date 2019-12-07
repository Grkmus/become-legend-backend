FROM continuumio/miniconda3:latest

RUN apt-get update -y && \
    apt-get install -y python-pip python-dev && \
    pip install --upgrade pip setuptools

# We copy this file first to leverage docker cache
COPY ./requirements.txt /become-legend/requirements.txt

WORKDIR /become-legend

COPY . /become-legend
RUN pip install -r requirements.txt
RUN pip install -e .

EXPOSE 6543
EXPOSE 8888