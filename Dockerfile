FROM ubuntu:latest
LABEL authors="danya"

ENTRYPOINT ["top", "-b"]