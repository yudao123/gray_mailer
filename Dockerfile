FROM python:3.6

EXPOSE 8000

RUN sed -i -s 's/deb.debian.org/mirrors.ustc.edu.cn/g' /etc/apt/sources.list
RUN apt-get update && apt-get install -y ca-certificates curl supervisor nginx vim

WORKDIR /opt/work
COPY requirements.txt /opt/work

RUN pip install -r requirements.txt -i https://pypi.doubanio.com/simple

VOLUME /data

COPY . /opt/work
CMD ["gunicorn", "-b", ":8000", "-w", "1", "app:app"]
