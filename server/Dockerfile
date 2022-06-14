FROM python:3

ADD server.py /

RUN pip install pycryptodome

ENV PORT=5050

EXPOSE 5050

CMD ["python", "./server.py"]