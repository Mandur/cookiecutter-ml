#!/usr/bin/env bash


echo "Running Tests"

#Run the docker test stage
appname=$(jq -r .application.name .pipelines/pipeline.json)
docker build -t $appname . --target test

