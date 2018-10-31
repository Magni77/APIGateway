FROM python:3.6.5-slim

# set the working directory in the container to /app
WORKDIR /app

# add the current directory to the container as /app
ADD . /app

RUN pip install -r requirements.txt


CMD ["python", "app.py"]
