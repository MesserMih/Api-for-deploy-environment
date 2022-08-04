FROM python:3.9-alpine
WORKDIR /opt
COPY ./core/requirements.txt /opt/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /opt/requirements.txt
COPY . .
#CMD ["python3", "main.py"]