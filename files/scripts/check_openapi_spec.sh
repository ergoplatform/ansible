#!/usr/bin/env sh

pip3 install ansicolors openapi-spec-validator
wget -N https://raw.githubusercontent.com/ergoplatform/ansible/master/files/scripts/validator.py
npm i speccy

# Python OpenAPI validator
echo
echo "Validating with Python openapi-spec-validator..."
python3 validator.py src/main/resources/api/openapi.yaml

# NodeJS OpenAPI validator
echo
echo "Validating with NodeJS speccy..."
node_modules/.bin/speccy lint -s openapi-tags src/main/resources/api/openapi.yaml
