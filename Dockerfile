FROM python:3-slim

COPY requirements.txt /tmp/requirements.txt

RUN pip install -r /tmp/requirements.txt
# Dummy command to keep container from exiting
CMD python -m http.server
