FROM ubuntu:16.04
# Update and install python
RUN apt-get update -y && \
    apt-get install -y python3-pip python3
ENTRYPOINT ["python3"]
RUN mkdir /app
ADD . /app
WORKDIR /app
# Install fing
RUN dpkg -i files/fing-5.5.2-amd64.deb
# Upgrade pip to version 21
RUN pip3 install --upgrade "pip < 21.0" 
#install requirements
RUN pip3 install -r requirements.txt
# RUN app
CMD ["app.py"]