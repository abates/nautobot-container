ARG NAUTOBOT_VER=1.2.5
ARG PYTHON_VER=3.8

FROM ghcr.io/nautobot/nautobot:${NAUTOBOT_VER}-py${PYTHON_VER}
LABEL org.opencontainers.image.source=https://github.com/abates/nautobot-container
ARG BUILDPLATFORM
ARG TARGETARCH=amd64
ARG S6_REPO=https://github.com/just-containers/s6-overlay/releases/download
ARG S6_VER=3.0.0.2
ARG NAUTOBOT_ROOT=/opt/nautobot
ENV NAUTOBOT_ROOT ${NAUTOBOT_ROOT}
WORKDIR $NAUTOBOT_ROOT

USER root
RUN apt-get -y update && \
    apt-get -y upgrade && \
    apt-get install --no-install-recommends -y xz-utils curl && \
    apt-get clean all && \
    rm -rf /var/lib/apt/lists/* 

RUN curl -sf -L ${S6_REPO}/v${S6_VER}/s6-overlay-noarch-${S6_VER}.tar.xz --output /tmp/s6-overlay-noarch.tar.xz && \
    tar -C / -Jxpf /tmp/s6-overlay-noarch.tar.xz

RUN curl -sf -L ${S6_REPO}/v${S6_VER}/s6-overlay-$(if [ "$TARGETARCH" = 'amd64' ] ; then echo 'x86_64' ; else echo "$TARGETARCH" ; fi)-${S6_VER}.tar.xz -o /tmp/s6-overlay.tar.xz && \
    tar -C / -Jxpf /tmp/s6-overlay.tar.xz 

COPY root/ /

ENV S6_GLOBAL_PATH /command:/usr/local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
ENV S6_KEEP_ENV 1
ENV S6_CMD_WAIT_FOR_SERVICES_MAXTIME 0
ENTRYPOINT ["/init"]
