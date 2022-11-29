#!/usr/bin/env bash

echo "Training model"

pipeline_name="job-$stage-$BUILD_NUMBER"
az ml job create --name $pipeline_name --file azureml/job_pipeline.yml -o tsv --only-show-errors --query name --stream

echo "Evaluate model"

evaluate_model_job=$(az ml job list --parent-job-name $pipeline_name --query "[?display_name=='evaluate_job'].name" -o tsv)
az ml job download --name $evaluate_model_job --output-name evaluation_output_folder -p /tmp

min=0.7
acc=$(cat /tmp/named-outputs/evaluation_output_folder/accuracy.txt)

if [ 1 -eq "$(echo "${acc} < ${min}" | bc)" ]
then  
    echo 'Model does not meet the minimal ${min} accuracy score'
    exit 1
fi

echo "Registering model"

training_job=$(az ml job list --parent-job-name $pipeline_name --query "[?display_name=='training_job'].name" -o tsv)
az ml job download --name $training_job --output-name trained_model_folder -p /tmp
az ml model create --name "inference-model-$stage" --type "mlflow_model" --path /tmp/named-outputs/trained_model_folder

echo "Building container"

registry=$(jq -r .archive.registry .pipelines/pipeline.json)
repository=$(jq -r .archive.repository .pipelines/pipeline.json)

image="${registry}/${repository}:0.0.${BUILD_TAG}-${stage}"

echo "DEBUG: image name: $image"
cp /tmp/named-outputs/trained_model_folder/model.pkl src/inference/
docker login -u ${registry_user} -p ${registry_password} ${registry}
docker build -t $image src/inference/

echo "Pushing container"
docker push "${image}"