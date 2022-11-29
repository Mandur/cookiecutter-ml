#!/usr/bin/env bash

echo "Publishing Application containers"

registry=$(jq -r .archive.registry .pipelines/pipeline.json)
repository=$(jq -r .archive.repository .pipelines/pipeline.json)

image="${registry}/${repository}:${BUILD_TAG}"

echo "DEBUG: image name: $image"

docker build -t "${image}" .
docker push "${image}"