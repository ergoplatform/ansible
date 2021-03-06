Deploy Ergo Node to Testnet or Mainnet via Jenkins
==================================================

This manual describes how you can deploy specific build of Ergo node to Testnet or Mainnet.


## Features and limitations

- Ergo node `master` branch automatically deployed to Testnet after integration tests successfully done
- There is no automatic deploy to Mainnet of any kind
- You should manually follow instructions below to deploy to Mainnet, as to deploy specific (not `master`) branch to Testnet
- You can not deploy builds older than 60 days
- You can not deploy builds that has unfinished [Integration tests](https://jenkins.ergoplatform.com/job/ergo-it/) jobs
- [Integration tests](https://jenkins.ergoplatform.com/job/ergo-it/) must be successfully done for deploying build, at least, `sbt` compilation must ended up successfully. But it is strongly recommended never deploy failed builds
- Passing of configuration files to deploy is not supported now. Because of this, all nodes in Mainnet and Testnet has as general configs as possible. Configs files are placed under [files/configs/ergo-testnet](../files/configs/ergo-testnet) for Testnet and config file template [files/configs/ergo-mainnet](../files/configs/ergo-mainnet/application.conf.j2) for Mainnet and periodically updated via Ansible. Feel free to [create issue](https://github.com/ergoplatform/ansible/issues/new) to add the ability to pass configs with deploys


## Deploy scripts and details

Mainnet and Testnet deploy script use same script that located here: [files/scripts/jenkins/ergo-deploy-to-mainnet-or-testnet/ergocicd.sh](../files/scripts/jenkins/ergo-deploy-to-mainnet-or-testnet/ergocicd.sh)


## Ergo nodes files location

According to [Deploy script](../files/scripts/jenkins/ergo-deploy-to-mainnet-or-testnet/ergocicd.sh), files are placed under `/data/ergo` directory:

- node .jar file: `/data/ergo/ergo.jar`
- node data dir:  `/data/ergo/.ergo`
- config file:    `/data/ergo/application.conf`
- node log file:  `/data/ergo/ergo.log`


## Manual

0. Make sure that `ergo-it` job is finished succesfully, since a deployment build is produced by `ergo-it`.

1. Click on [ergo-deploy-to-mainnet build button](https://jenkins.ergoplatform.com/job/ergo-deploy-to-mainnet/build?delay=0sec) to start deploying Ergo node to Mainnet (or click on [ergo-deploy-to-testnet build button](https://jenkins.ergoplatform.com/job/ergo-deploy-to-testnet/build?delay=0sec) to deploy to Testnet)

2. You will see build parameters form with 3 fields:

    - **WIPEDATA** checkbox (default is unchecked): if checked, node main data folder will be wiped, and node start syncing with blockchain from scratch

    - **VERSION** string (default is `master`): the branch name which build must be deployed (only branch names are supported, no tags nor commits names)

    - **NODE** select box (all nodes are selected by default): on which nodes deploy given build

3. After tuning above paramaters, press **Build** button. Selected Ergo node build start deploying to chosen node(s), sequentually, one by one.

That's all! You also can:

- Track the deploy logs as usual Jenkins job logs with Jenkins job **Build history**.
- Track and monitor build behaviour with Grafana: [Mainnet](https://grafana.ergoplatform.com/d/OwXtQiNZz) or [Testnet](https://grafana.ergoplatform.com/d/000000001)
- Track Ergo node logs on chosen host: ssh on it (see [inventory](../inventory/hosts) for IP and ask admins for credentials), then use `tail`. Example: `tail -f /data/ergo/ergo.log`)
- Monitor hosts CPU load, memory consumption and other system parameters: [Overall hosts statistics](https://grafana.ergoplatform.com/d/M-Xtpr5mz/overall)


## Troubleshooting

> The deployment CI job always gets the latest available build from specified branch, right?

Right. So be attentive, if you run deploy before `ergo-it` is finished, it may deploy unexpected (outdated) build (or can not deploy it at all, since there are no builds yet). On the other hand, you may want deploy outdated build and see results, when next build is under testing, and you have that ability.

> If I update my ergo branch and run ergo-it job and after that run deploy it’ll pick up the the last build, correct?

Absolutely correct. When `ergo-it` job finished (and at least compilation phase of the job was succesfull), the last build of specific branch is the result of finished `ergo-it` job of specific branch, and exactly that version be deployed on next deploy for specific branch.
