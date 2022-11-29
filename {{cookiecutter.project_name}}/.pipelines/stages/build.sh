#!/usr/bin/env bash

echo "Building Application"

appname=$(jq -r .application.name .pipelines/pipeline.json)
docker build -t $appname . --target build