#!/usr/bin/env sh

MAXWAIT=30
RUNPATH=/home/ergo/node/ergo.jar
NODE_JAR=/home/ergo/node/ergo.jar
NODE_CONFIG=/home/ergo/node/application.conf
NODE_LOG=/home/ergo/node/l.log
PID=$(pgrep -f ${RUNPATH})
FOUND=$?

sbt reload clean assembly

set -e

if echo ${PID} | grep -q ' '; then

    echo "Error: More than one process found. Quitting." >&2
    exit 1

elif [ "${FOUND}" -eq 0 ] && [ -n "${PID}" ]; then

    if ! kill ${PID}; then
        echo "Error: Am not allowed to kill process ${PID}. Quitting." >&2
        exit 2
    fi

    echo "Killing process ${PID} and wait ${MAXWAIT} seconds until it die"
    i=0
    while kill -0 ${PID}; do
        if [ "$i" -gt "${MAXWAIT}" ]; then
            echo "Error: Waited more than ${MAXWAIT} seconds for process with pid ${PID} to die. Giving up." >&2
            exit 3
        fi
        i=$((i + 1))
        sleep 1
    done

fi

echo "Starting Ergo node..."

cp -pf $(find /home/ergo/jenkins -name ergo-assembly*.jar) ${NODE_JAR}

#java -Xmx3G --add-modules java.xml.bind -jar ${NODE_JAR} ${NODE_CONFIG} > ${NODE_LOG} 2>&1 &
java -jar ${NODE_JAR} ${NODE_CONFIG} > ${NODE_LOG} 2>&1 &
