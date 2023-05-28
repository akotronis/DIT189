FROM python:3.10-alpine3.17

RUN apk update && apk add gcc libc-dev && apk add bash

WORKDIR /usr/data/app

# Set environment varibles
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# RUN addgroup -S appuser && adduser -S appuser -G appuser  --home /usr/data

ENV PATH=$PATH:/usr/data/.local/bin

COPY ./requirements.txt .

COPY . .
RUN pip install -r requirements.txt

# RUN chown -R appuser:appuser /usr/data

# USER appuser:appuser

EXPOSE 5000/tcp

CMD ["/bin/bash", "entrypoint.sh"]

# Keep the container running for debugging purposes
# ENTRYPOINT ["tail", "-f", "/dev/null"]
