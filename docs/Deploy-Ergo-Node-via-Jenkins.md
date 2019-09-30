Deploy Ergo Node to Testnet or Mainnet via Jenkins
==================================================

This manual describes how you can deploy specific build of Ergo node to Testnet or Mainnet.


## Features and limitations

- Ergo node `master` branch build automatically deployed to Testnet after integration tests successfully done
- There is no automatic deploy to Mainnet of any kind
- You should manually follow that instructions to deploy to Mainnet, as to deploy specific (not `master`) branch to Testnet
- You can not deploy builds older than 60 days


## Manual

1. Click on [ergo-deploy-to-mainnet build button](https://jenkins.ergoplatform.com/job/ergo-deploy-to-mainnet/build?delay=0sec) to start deploying Ergo node to Mainnet (or click on [ergo-deploy-to-testnet build button](https://jenkins.ergoplatform.com/job/ergo-deploy-to-testnet/build?delay=0sec) to deploy to Testnet)

2. You will see build parameters form with 3 fields:

    - **WIPEDATA** checkbox (default is unchecked): if checked, node main data folder will be wiped, and node start syncing with blockchain from scratch

    - **VERSION** string (default is `master`): the branch name which build must be deployed (only branch names are supported, no tags nor commits names)

    - **NODE** select box (all nodes are selected by default): on which nodes deploy given build

3. After tuning above paramaters, press **Build** button. Selected Ergo node build start deploying to chosen node(s), sequentually, one by one.

That's all! You also can:

- Track the deploy logs as usual Jenkins job logs with Jenkins job **Build history**.
- Track and monitor build behaviour with Grafana: [Mainnet](https://grafana.ergoplatform.com/d/OwXtQiNZz) or [Testnet](https://grafana.ergoplatform.com/d/000000001)
