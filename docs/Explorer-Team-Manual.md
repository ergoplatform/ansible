Explorer Team Manual
====================

This manual address deploy and troubleshooting workflow for Explorer.


## Basics

Explorer consists of two separate projects: [Backend](https://github.com/ergoplatform/explorer-back) and [Frontend](https://github.com/ergoplatform/ergo-explorer). Backend need a PostgreSQL database to store and index blockchain data. Frontend can run on it's own, without any dependencies.

Testnet and Mainnet Explorer stacks executes on dedicated servers. See [inventory/hosts](https://github.com/ergoplatform/ansible/blob/04446f782455cc645b992fd954be5285bbda2286/inventory/hosts#L6) for `explorer` host (Testnet) and `explorer-mainnet` host (Mainnet).


## Deploy

Explorer deployed as [Docker Swarm Stack](https://docs.docker.com/get-started/part4/). You can see stack definitions here:

- [Explorer Testnet Docker Swarm Stack](../files/stacks/explorer.yml)
- [Explorer Mainnet Docker Swarm Stack](../files/stacks/explorer-mainnet.yml)

There is also configurations for Explorers:

- [Explorer Testnet Configs](../files/configs/ergo-explorer)
- [Explorer Mainnet Configs](../files/configs/ergo-explorer-mainnet)

Note that some configuration exists as environment variables and stored in Docker Swarm Stack definitions.


### Autodeploy

Autodeploy configuration placed [here](../files/configs/dockerhub-webhooks/config.json).

Testnet autodeploy happens on any push event in mentioned projects `master` branch. Github send push event to [Docker Hub](https://hub.docker.com/), when Docker Hub builds new project image, it sends webhook to our autodeploy facility, and autodeploy execute `docker stack deploy -c explorer.yml explorer` for Testnet.

Mainnet autodeploy happens on any push event in `mainnet` branch of mentioned projects, and deploys with `docker stack deploy -c explorer-mainnet.yml explorer-mainnet` command.


## Troubleshooting

In case of any problems with explorers, you can try following:

1. ssh on `explorer` or `explorer-mainnet` with your credentials (reference with [hosts inventory](../inventory/hosts) for hosts IP, [explorers hosts users](../inventory/group_vars/explorers/users) for credentials)

2. Execute `sudo docker container ps -a` to see which containers are running now and which are exited. You can visually figure out the container of your interest and find its `<CONTAINER_ID>`.

3. Execute `sudo docker container logs -f --tail 100 <CONTAINER_ID>` to see container's logs. Choose `CONTAINER_ID` from previous step.

4, Execute `sudo docker container stop <CONTAINER_ID>` to stop stucked container. Docker Swarm automatically start another container to fits stack definition needs. Container you stopped remains, and you can explore its logs later.
