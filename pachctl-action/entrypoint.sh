#!/bin/bash

set -e

if [ -z "$PACHYDERM_TOKEN" ]; then
  echo "PACHYDERM_TOKEN is not set. Quitting."
  exit 1
fi

if [ -z "$PACHYDERM_CLUSTER_URL" ]; then
  echo "PACHYDERM_CLUSTER_URL is not set. Quitting."
  exit 1
fi
if [ -z "$VERSION" ]; then
  echo "VERSION is not set. Getting Latest."
  V=$(wget -qO -  https://api.github.com/repos/pachyderm/pachyderm/releases/latest | jq -r ".tag_name")
  VERSION=${V:1}
  echo "Using ${VERSION} pachctl version."
fi

if [ -z "$PACHYDERM_CLUSTER_URL" ]; then
  echo "PACHYDERM_CLUSTER_URL is not set. Quitting."
  exit 1
fi
wget -O pachctl.tar.gz https://github.com/pachyderm/pachyderm/releases/download/v${VERSION}/pachctl_${VERSION}_linux_amd64.tar.gz 
tar -xzf pachctl.tar.gz --strip-components=1
mv pachctl /usr/local/bin/pachctl

echo '{"pachd_address": "'${PACHYDERM_CLUSTER_URL}'"}' | pachctl config set context default --overwrite
echo ${PACHYDERM_TOKEN} | pachctl auth use-auth-token

pachctl ${COMMAND}
