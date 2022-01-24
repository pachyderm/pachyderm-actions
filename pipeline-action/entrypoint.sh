#!/bin/bash

echo '{"pachd_address": "'${PACHYDERM_CLUSTER_URL}'"}' | pachctl config set context default --overwrite
echo ${PACHYDERM_TOKEN} | pachctl auth use-auth-token
for pipeline in  ${PACHYDERM_PIPELINE_FILES}
do
    # even if the pipeline doesn't exist, this will create it.
    jq --arg tag ${DOCKER_IMAGE_NAME}  --arg version ${GITHUB_SHA} '.transform.image |= $tag+":"+$version' ${pipeline} | pachctl update pipeline
done

