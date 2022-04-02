FROM python:alpine

WORKDIR /schedule-kubsau-parser

ADD . /schedule-kubsau-parser

RUN pip install -r requirements.txt

CMD [ "python", "-u", "main.py" ]
