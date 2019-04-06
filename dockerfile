FROM alpine:3.9

ADD main.py /
ADD requirements.txt /

RUN apk add --no-cache python3 gcc python3-dev musl-dev && \
    python3 -m ensurepip && \
    rm -r /usr/lib/python*/ensurepip && \
    pip3 install --upgrade pip setuptools && \
    if [ ! -e /usr/bin/pip ]; then ln -s pip3 /usr/bin/pip ; fi && \
    if [[ ! -e /usr/bin/python ]]; then ln -sf /usr/bin/python3 /usr/bin/python; fi && \
    rm -r /root/.cache && \
    pip install -r requirements.txt && \
    apk del gcc python3-dev musl-dev && \
    pip3 uninstall pip -y

CMD [ "python", "./main.py" ]
