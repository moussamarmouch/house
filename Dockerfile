FROM ubuntu:16.04
RUN apt-get update -y && \
    apt-get install -y python3-pip python3-dev
RUN mkdir /app
RUN mkdir /install
ADD . /app
ADD files /install
WORKDIR /install
RUN dpkg -i fing-5.5.2-amd64.deb
WORKDIR /app
RUN pip3 install --upgrade pip
RUN pip install -r requirements.txt
CMD ["python", "app.py"]