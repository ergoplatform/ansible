#!/usr/bin/env sh

MAXWAIT=60
WASKILL9=false
NODE_BASE_DIR=/data/ergo
NODE_JAR=${NODE_BASE_DIR}/ergo.jar
NODE_CONFIG=${NODE_BASE_DIR}/application.conf
NODE_LOG=${NODE_BASE_DIR}/ergo_norotate.log
NODE_PARAMS="-XX:+HeapDumpOnOutOfMemoryError -XX:HeapDumpPath=/tmp/java_build_id${BUILD_ID}.hprof"
NODE_DATA_DIR=${NODE_BASE_DIR}/data
PIDS=$(pgrep -f "ergo.*\.jar")
FOUND=$?
WIPEDATA=${WIPEDATA:-false}
VERSION=${VERSION:-master}
JARFILE_TO_SEEK="ergo-deploy-to-testnet-${VERSION}.jar"

# Variable INFLUXDB_CONNECTION_STRING should exists for curling to InfluxDB monitoring database
# Variables BUILD_ID, BUILD_TAG, BUILD_URL and others are provided by Jenkins

# This script does not work with `set -xe`

if echo ${PIDS} | grep -q ' '; then
    echo "Error: More than one process found. Killing processes ${PIDS} subsequentially, one by one." >&2
fi

for pid in ${PIDS}
do
    if [ "${FOUND}" -eq 0 ] && [ -n "${pid}" ]; then

        if ! kill ${pid}; then
            echo "Error: Am not allowed to kill process ${pid}. Quitting." >&2
            exit 2
        fi

        echo "Killing process ${pid} and wait ${MAXWAIT} seconds until it die"
        i=0
        while kill -0 ${pid}; do
            if [ "$i" -gt "${MAXWAIT}" ]; then
                echo "Error: Waited more than ${MAXWAIT} seconds for process with pid ${pid} to die." >&2
                if [ "$WASKILL9" = true ] ; then
                    echo "Error: Waited more than ${MAXWAIT} seconds after kill -9 ${pid}. Giving up." >&2
                    exit 3
                else
                    echo "Trying kill -9 ${pid} and wait another ${MAXWAIT} seconds until it die..."
                    kill -9 ${pid}
                    WASKILL9=true
                    i=0
                fi
            fi
            i=$((i + 1))
            sleep 1
        done

    fi
done

if ${WIPEDATA}; then
    echo "Wiping node data..."
    rm -rf ${NODE_DATA_DIR}
    echo "Done."
fi

echo "Starting Ergo node..."

cp -pf $(find . -type f -name ${JARFILE_TO_SEEK}) ${NODE_JAR}

if [ "$(hostname)" = 'testnet1-light-ubuntu-s-1vcpu-2gb-lon1-01' ]; then
    NODE_PARAMS="-Xmx2G ${NODE_PARAMS}"
else
    NODE_PARAMS="-Xmx4G ${NODE_PARAMS}"
fi

BUILD_ID=dontKillMe nohup java ${NODE_PARAMS} -jar ${NODE_JAR} ${NODE_CONFIG} > ${NODE_LOG} &

# Supress passwords output used below
set +xe

# Read the INFLUXDB_CONNECTION_STRING variable if it exists
if [ -f /etc/profile.d/testnet_env_vars.sh ]; then
    . /etc/profile.d/testnet_env_vars.sh

    # If this variable was read, then report about event to InfluxDB
    if [ -n ${INFLUXDB_CONNECTION_STRING} ]; then
        INFLUXDB_EVENT_TITLE="Deployed ${VERSION} on $(hostname)"
        INFLUXDB_EVENT_DESCRIPTION="<a href='${BUILD_URL}'>Build info</a>"
        curl -s -X POST ""${INFLUXDB_CONNECTION_STRING}"" --data-binary 'events title="'"${INFLUXDB_EVENT_TITLE}"'",description="'"${INFLUXDB_EVENT_DESCRIPTION}"'"'
    fi
fi
