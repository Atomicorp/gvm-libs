FROM ubuntu:18.04

MAINTAINER support <support@atomicorp.com>

RUN sed -i 's/^# deb-src \(.*bionic.* main restricted\)$/deb-src \1/g' /etc/apt/sources.list

RUN apt-get update

RUN apt-get build-dep -y linux 
RUN apt-get install -y fakeroot devscripts bc  debhelper bison cmake doxygen libgcrypt-dev libglib2.0-dev libgnutls28-dev libgpgme11-dev libhiredis-dev libksba-dev libldap2-dev libpcap-dev libssh-dev uuid-dev libsnmp-dev
RUN apt-get clean 

RUN install --directory -m 0755 /data && \
    install --directory -m 0755 /patches


WORKDIR /data

VOLUME /data
VOLUME /patches

RUN groupadd -r gitlab-runner -g 478
RUN useradd -u 480 -r -g gitlab-runner gitlab-runner

# we have to run as root so that we can apt-get update
ENTRYPOINT ["/data/builder.sh"]
