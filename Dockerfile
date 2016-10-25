FROM alpine:3.4
RUN apk --no-cache add python
RUN mkdir -p /opt/python\
 && addgroup -g 1000 python\
 && adduser -h /home/python -u 1000 -G python -D -s /bin/false python\
 && chown -R python:python /opt/python
USER python
WORKDIR /opt/python
COPY start.sh /
COPY selector.py /opt/python/
COPY lib/*.py /opt/python/lib/
ENTRYPOINT ["/start.sh"]
