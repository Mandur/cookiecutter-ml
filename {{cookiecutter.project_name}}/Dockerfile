FROM python:3.10 as base
WORKDIR /code

FROM base as dependencies
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copying files from root directory to working directory
# Build stage
FROM dependencies as build
WORKDIR /code
COPY . .

FROM build as test
RUN flake8 src/model/
RUN pytest tests