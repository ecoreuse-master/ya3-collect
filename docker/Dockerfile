# Copyright (c) 2022 Shuhei Nitta. All rights reserved.
FROM python:3.10-bullseye as builder

WORKDIR /opt
COPY ya3-collect.tar.gz .
RUN pip install -U pip \
 && pip install ya3-collect.tar.gz

FROM python:3.10-slim-bullseye as runner
COPY --from=builder /usr/local/bin/ya3-collect /usr/local/bin/ya3-collect
COPY --from=builder /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages

WORKDIR /ya3
ENV PYTHONUNBUFFERED 1

ENTRYPOINT [ "ya3-collect" ]