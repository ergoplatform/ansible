#!/usr/bin/env sh

set -e

SPEC_IS_WRONG=false

pip3 install ansicolors openapi-core openapi-spec-validator
wget -N https://raw.githubusercontent.com/ergoplatform/ansible/master/files/scripts/check_openapi_spec.py
wget -N https://raw.githubusercontent.com/ergoplatform/ansible/master/files/scripts/check_openapi_responses.py
npm i speccy

# Python OpenAPI validator
echo
echo "Validating with Python openapi-spec-validator..."
python3 check_openapi_spec.py src/main/resources/api/openapi.yaml
if [ $? -ne 0 ]; then
    SPEC_IS_WRONG=true
fi

# NodeJS OpenAPI validator
echo
echo "Validating with NodeJS speccy..."
node_modules/.bin/speccy lint -s openapi-tags src/main/resources/api/openapi.yaml
if [ $? -ne 0 ]; then
    SPEC_IS_WRONG=true
fi

# Exiting if OpenAPI specification did not pass validation
if ${SPEC_IS_WRONG}; then
    echo "OpenAPI specification is wrong, exiting..."
    exit 1
fi

python3 check_openapi_responses.py src/main/resources/api/openapi.yaml
