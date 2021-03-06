#!/usr/bin/env sh

BRANCH=$(git branch -r --contains ${GIT_COMMIT} 2> /dev/null)
BRANCH_EXISTS=$?
BRANCHES_COUNT=$(echo $BRANCH | wc -l)
COMMIT_IN_MASTER=$(git branch -r --contains ${GIT_COMMIT} | grep -ni 'origin/master')
COMMIT_IN_MASTER=$?
ERGO_NODE_FILENAME_PATTERN=ergo-*.jar

# ${GIT_COMMIT} variable is provided by Jenkins

echo "Branch: ${BRANCH}"
echo "Exists?: ${BRANCH_EXISTS}"
echo "Count: ${BRANCHES_COUNT}"
echo "In master?: ${COMMIT_IN_MASTER}"

if [ "${COMMIT_IN_MASTER}" != 0 ]; then
    echo "Commit ${GIT_COMMIT} is not in master branch"

    if [ "${BRANCH_EXISTS}" != 0 ]; then
        echo "Commit ${GIT_COMMIT} is not exists at all, skipping!"
        exit 1
    elif [ "${BRANCHES_COUNT}" != 1 ]; then
        echo "Branches count for commit ${GIT_COMMIT} is not equal to 1 but equals to ${BRANCHES_COUNT}, skipping!"
        exit 2
    else
        echo "Commit ${GIT_COMMIT} is in branch ${BRANCH}"
        BRANCH=$(echo "${BRANCH}" | sed -e 's/^[[:space:]]*origin.[[:space:]]*//' | tr -d '[:space:]')
        filename="ergo-deploy-to-testnet-${BRANCH}.jar"
        rc=3
    fi

else
    echo "Commit ${GIT_COMMIT} is in master branch"
    filename="ergo-deploy-to-testnet-master.jar"
    rc=0
fi

echo "Delete outdated ${filename}..."
rm -f "${filename}"
echo
echo "There are following .jar files in target directory (hash and filename):"
find target -type f -name "${ERGO_NODE_FILENAME_PATTERN}" -exec md5sum {} \;
echo
echo "Copy current build .jar file to ./${filename} (actually the last printed filename copied)"
find target -type f -name "${ERGO_NODE_FILENAME_PATTERN}" -print -exec cp -pf {} "${filename}" \;
exit ${rc}
