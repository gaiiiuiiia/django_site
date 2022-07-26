FROM python:3.10-slim

RUN apt-get update \
    && apt-get install -y postgresql \
    && apt-get install -y gcc \
    && apt-get install -y python3-dev \
    && apt-get install -y musl-dev

ARG UID=1000
ARG GID=1000
ARG UNAME=appuser
RUN set -x ; \
    groupadd --gid ${GID} ${UNAME}; \
    useradd --uid ${UID} --gid ${GID} -m ${UNAME} && exit 0 ; exit 1

ARG APP_DIR=/var/www/app
WORKDIR ${APP_DIR}

COPY --chown=${UID}:${GID} . .

RUN python -m pip install --upgrade pip \
    && pip install -r requirements.txt

USER ${UNAME}
