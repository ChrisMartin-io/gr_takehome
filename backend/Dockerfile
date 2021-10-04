# start from base
FROM ubuntu:18.04

# install system-wide deps for python and node
RUN apt-get -yqq update
RUN apt-get -yqq install python3-pip python3-dev curl gnupg

ADD ./ /opt/grabango/backend
WORKDIR /opt/grabango/backend

# install dependencies
RUN pip3 install -r requirements.txt

EXPOSE 5000

CMD ['flask', 'run']