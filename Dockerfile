FROM hub.c.163.com/library/centos:7.4.1708

COPY ./ /opt/server/consolemg


RUN groupadd -g 2000 server &&\
    useradd -u 2000 -g  2000 server &&\
    rm -rf /root/* &&\
    mv /opt/server/consolemg/entrypoint.sh /bin &&\
    chmod +x /bin/entrypoint.sh &&\
    find /opt/server -type d -exec chmod o=--- {} \; &&\
    find /opt/server -type f -exec chmod o=--- {} \; &&\
    chown 2000:2000 -R /opt/server


USER server

WORKDIR /opt/server/consolemg
ENTRYPOINT ["entrypoint.sh"]
