FROM python:2.7
WORKDIR /usr/local/application/
COPY . /usr/local/application/
RUN mkdir -p /usr/local/logs
RUN pip install -r requirements.txt
CMD [ "python" ,"manage.py","runserver", "0.0.0.0:51234"]