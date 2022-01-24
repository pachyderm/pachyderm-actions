FROM python:3.8.12
RUN pip install python-pachyderm certifi networkx
COPY *.py /

ENTRYPOINT ["/pipeline_update.py"]
