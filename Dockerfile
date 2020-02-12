# We're using Alpine stable
FROM alpine:edge

#
# We have to uncomment Community repo for some packages
#
RUN sed -e 's;^#http\(.*\)/v3.9/community;http\1/v3.9/community;g' -i /etc/apk/repositories

# Installing Python
RUN apk add --no-cache --update \
    bash \
    bzip2-dev \
    gcc \
    g++ \
    git \
    sudo \
    python3 \
    python3-dev \

RUN pip3 install --upgrade pip setuptools

RUN git clone -b master https://github.com/Prakasaka/PaperplaneExtended /home/userbot/userbot
WORKDIR /home/userbot/userbot
ADD ./requirements.txt /home/userbot/userbot/requirements.txt

#
# Copies session and config(if it exists)
#
COPY ./sample_config.env ./userbot.session* ./config.env* /home/userbot/userbot/

#
# Clone helper scripts
#
# RUN curl -s https://raw.githubusercontent.com/yshalsager/megadown/master/megadown -o /home/userbot/bin/megadown && sudo chmod a+x /home/userbot/bin/megadown
# RUN curl -s https://raw.githubusercontent.com/yshalsager/cmrudl.py/master/cmrudl.py -o /home/userbot/bin/cmrudl && sudo chmod a+x /home/userbot/bin/cmrudl
# ENV PATH="/home/userbot/bin:$PATH"

#
# Install requirements
#
RUN sudo pip3 install -r requirements.txt
ADD . /home/userbot/userbot
RUN sudo chown -R userbot /home/userbot/userbot
RUN sudo chmod -R 777 /home/userbot/userbot
CMD ["python3","-m","userbot"]
