# We're using Alpine stable
FROM alpine:edge

#
# We have to uncomment Community repo for some packages
#
RUN sed -e 's;^#http\(.*\)/v3.9/community;http\1/v3.9/community;g' -i /etc/apk/repositories

# install ca-certificates so that HTTPS works consistently
# other runtime dependencies for Python are installed later
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
    util-linux \
    libevent \
    jpeg-dev \
    libffi-dev \
    libpq \
    libwebp-dev \
    libxml2 \
    libxml2-dev \
    libxslt-dev \
    linux-headers \
    musl \
    openssl-dev \
    postgresql \
    postgresql-client \
    postgresql-dev \
    openssl \
    pv \
    jq \
    wget \
    python \
    python3 \
    python3-dev \
    readline-dev \
    sqlite \
    sqlite-dev \
    zlib-dev \
    jpeg-dev \
    python-dev

RUN pip3 install --upgrade pip setuptools



RUN git clone https://github.com/Prakasaka/PaperplaneExtended /root/userbot
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
