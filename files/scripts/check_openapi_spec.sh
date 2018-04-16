#!/usr/bin/env sh

pip3 install ansicolors openapi-spec-validator
wget -N https://raw.githubusercontent.com/ergoplatform/ansible/master/files/scripts/validator.py
python3 validator.py src/main/resources/api/openapi.yaml
