FROM python:3.12-alpine3.21

# Copy requirements and install dependencies
COPY requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install --no-cache-dir -r requirements.txt

# Copy the appropriate main.py based on the build argument
ARG VERSION
COPY ${VERSION}/main.py /app/main.py
COPY logging_config.json /app/logging_config.json

ENTRYPOINT ["python", "/app/main.py"]