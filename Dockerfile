FROM python:2.7-alpine
ENV PYTHON_UNBUFFERED 1
RUN pip install requests
ENTRYPOINT ["/usr/bin/python", "/cli.py"]
