ARG NAUTOBOT_VERSION
ARG PYTHON_VER
FROM ghcr.io/nautobot/nautobot:${NAUTOBOT_VERSION}-py${PYTHON_VER} as nautobot-base

USER 0

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get autoremove -y && \
    apt-get clean all && \
    rm -rf /var/lib/apt/lists/* && \
    pip --no-cache-dir install --upgrade pip wheel

FROM ghcr.io/nautobot/nautobot-dev:${NAUTOBOT_VERSION}-py${PYTHON_VER} as nautobot-dev

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get autoremove -y && \
    apt-get clean all && \
    rm -rf /var/lib/apt/lists/*

COPY ./ /source/

# Install the nautobot project to include Nautobot
RUN cd /source && \
    poetry install --no-directory --no-interaction --no-ansi && \
    mkdir /tmp/dist && \
    poetry export --without-hashes -o /tmp/dist/requirements.txt && \
    pip uninstall -y nautobot-container

# -------------------------------------------------------------------------------------
# Install tools
# -------------------------------------------------------------------------------------
SHELL ["/bin/bash", "-o", "pipefail", "-c"]
WORKDIR /source
RUN rm -rf dist/ && \
    poetry build && \
    pip install dist/*.whl && \
    cp dist/*.whl /tmp/dist

COPY nautobot_config.py /opt/nautobot/nautobot_config.py
COPY nautobot-deployment-entrypoint.sh /nautobot-deployment-entrypoint.sh
ENTRYPOINT ["/nautobot-deployment-entrypoint.sh"]

WORKDIR /source

###################################

# -------------------------------------------------------------------------------------
# Final Image
# -------------------------------------------------------------------------------------
FROM nautobot-base as nautobot

# Copy from base the required python libraries and binaries
COPY --from=nautobot-dev /tmp/dist /tmp/dist
COPY --from=nautobot-dev /opt/nautobot /opt/nautobot
# COPY ./packages /source/packages

RUN pip install -r /tmp/dist/requirements.txt && \
    if [ -n "$(ls /tmp/dist/*.whl 2>/dev/null)" ] ; then pip install /tmp/dist/*.whl ; fi && \
    rm -rf /source && \
    chown -R nautobot:nautobot /opt/nautobot

COPY nautobot-deployment-entrypoint.sh /nautobot-deployment-entrypoint.sh
ENTRYPOINT ["/nautobot-deployment-entrypoint.sh"]
CMD ["nautobot-server", "start", "--ini", "/opt/nautobot/uwsgi.ini"]

USER nautobot
