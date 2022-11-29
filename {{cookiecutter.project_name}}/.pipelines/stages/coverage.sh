#!/usr/bin/env bash

echo "Code coverage"

#output code coverage details for pipeline to process

appname=$(jq -r .application.name .pipelines/pipeline.json)
docker create --name coverage $appname
docker cp coverage:/code/coverage.xml .
docker cp coverage:/code/unit_tests.xml .
docker rm -f coverage