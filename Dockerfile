# We're using Alpine stable
FROM alpine:edge

#
# We have to uncomment Community repo for some packages
#
RUN sed -e 's;^#http\(.*\)/v3.9/community;http\1/v3.9/community;g' -i /etc/apk/repositories

RUN apk add --no-cache ca-certificates

# Installing Python
RUN apk add --no-cache --update \
    bash \
    build-base \
    bzip2-dev \
    gcc \
    g++ \
    git \
    sudo \
    python3 \
    postgresql-client \
    postgresql-dev \
    sqlite-dev \
    python3-dev \
    python-dev

RUN git clone -b master https://github.com/Prakasaka/PaperplaneExtended /root/userbot
RUN mkdir /root/userbot/bin/
WORKDIR /root/userbot/

#
# Copies session and config (if it exists)
#
COPY ./sample_config.env ./userbot.session* ./config.env* /root/userbot/

#
# Install requirements
#
RUN pip3 install -r requirements.txt
CMD ["python3","-m","userbot"]
