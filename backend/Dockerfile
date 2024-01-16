FROM python3.9
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /starburger
COPY requirements.txt /starburger/
RUN apt update && apt install -y python3-pip                                  \
    && pip3 install -r requirements.txt                                       \
    && apt remove -y python3-pip                                              \
    && apt autoremove --purge -y                                              \
    && rm -rf /var/lib/apt/lists/* /etc/apt/sources.list.d/*.list

COPY ./ ./
WORKDIR /starburger/src
RUN python3 manage.py collectstatic --noinput
EXPOSE 80
VOLUME ["/media"]