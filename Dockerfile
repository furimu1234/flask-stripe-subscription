FROM python:3.10
USER root

RUN apt-get update
RUN apt-get -y install locales && \
    localedef -f UTF-8 -i ja_JP ja_JP.UTF-8
ENV LANG ja_JP.UTF-8
ENV LANGUAGE ja_JP:ja
ENV LC_ALL ja_JP.UTF-8
ENV TZ JST-9
ENV TERM xterm

RUN apt-get install less

WORKDIR /project
COPY ./requirements.txt /project

ADD ./src src

RUN pip install -Ur requirements.txt

EXPOSE 80

WORKDIR ./src
CMD ["python", "app.py"]
