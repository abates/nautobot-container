ARG NAUTOBOT_VER=1.2.5
ARG PYTHON_VER=3.8
FROM ghcr.io/nautobot/nautobot:${NAUTOBOT_VER}-py${PYTHON_VER}

ARG BUILDPLATFORM
ARG TARGETARCH=x86_64
ARG S6_VER=3.0.0.2
ARG NAUTOBOT_ROOT=/opt/nautobot
ENV NAUTOBOT_ROOT ${NAUTOBOT_ROOT}
WORKDIR $NAUTOBOT_ROOT

USER root
ADD https://github.com/just-containers/s6-overlay/releases/download/v${S6_VER}/s6-overlay-noarch-${S6_VER}.tar.xz /tmp
ADD https://github.com/just-containers/s6-overlay/releases/download/v${S6_VER}/s6-overlay-${TARGETARCH}-${S6_VER}.tar.xz /tmp
RUN apt-get -y update && \
    apt-get -y upgrade && \
    apt-get install --no-install-recommends -y xz-utils && \
    apt-get clean all && \
    rm -rf /var/lib/apt/lists/* && \
    tar -C / -Jxpf /tmp/s6-overlay-${TARGETARCH}-${S6_VER}.tar.xz && \
    tar -C / -Jxpf /tmp/s6-overlay-noarch-${S6_VER}.tar.xz

COPY root/ /

ENV S6_GLOBAL_PATH /command:/usr/local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
ENV S6_KEEP_ENV 1
ENV S6_CMD_WAIT_FOR_SERVICES_MAXTIME 0
ENTRYPOINT ["/init"]
