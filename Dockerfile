FROM python3.10
USER pi

RUN apt-get update
RUN apt-get -y install locales && \
localedef -f UTF-8 -i ja_JP ja_JP.UTF-8
ENV LANG ja_JP.UTF-8
ENV LANGUAGE ja_JP:ja
ENV LC_ALL ja_JP.UTF-8
ENV TZ JST-9
ENV TERM xterm

RUN apt-get install -y less

COPY requiremens.txt /project
COPY ./src project/src
WORKDIR /project

RUN pip install -Ur requiremens.txt
CMD ["python", "app.py"]
