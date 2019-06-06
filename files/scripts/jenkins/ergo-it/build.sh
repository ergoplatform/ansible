#!/usr/bin/env sh

find . -name ergo-assembly*.jar -delete
rm -rf target/logs/*.log
rm -rf /root/.ivy2/cache
docker container prune -f
docker image prune -f
sbt clean it:test
