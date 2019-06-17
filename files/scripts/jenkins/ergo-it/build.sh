#!/usr/bin/env sh

ERGO_NODE_FILENAME_PATTERN=ergo-*.jar

find target -type f -name "${ERGO_NODE_FILENAME_PATTERN}" -print -delete
find . -type f -name "${ERGO_NODE_FILENAME_PATTERN}" -mtime +60 -print -delete
rm -rf target/logs/*.log
rm -rf /root/.ivy2/cache
docker container prune -f
docker image prune -f
sbt clean it:test
