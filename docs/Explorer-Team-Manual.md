Explorer Team Manual
====================

This manual address deploy and troubleshooting workflow for Explorer.


## Basics

Explorer consists of two separate projects: [Backend](https://github.com/ergoplatform/explorer-back) and [Frontend](https://github.com/ergoplatform/ergo-explorer). Backend need a PostgreSQL database to store blockchain data and index it. Frontend can run on it's own, without any dependencies.

Testnet and Mainnet Explorer stacks executes on dedicated servers. See [inventory](../inventory/host) for `explorer` host (Testnet) and `explorer-mainnet` host (Mainnet).


## Deploy

Explorer deployed as [Docker Swarm Stack](https://docs.docker.com/get-started/part4/). You can see stack definitions here:

- [Explorer Testnet Docker Swarm Stack](../files/stacks/explorer.yml)
- [Explorer Mainnet Docker Swarm Stack](../files/stacks/explorer-mainnet.yml)

There is also configurations for Explorers:

- [Explorer Testnet Configs](../files/configs/ergo-explorer)
- [Explorer Mainnet Configs](../files/configs/ergo-explorer-mainnet)

Note that some configuration exists as environment variables and stored in Docker Swarm Stack definitions.


### Autodeploy

Autodeploy configuration placed [here](../files/configs/dockerhub-webhooks).

Testnet autodeploy happens on any push event in mentioned projects `master` branch. Github send push event to [Docker Hub](https://hub.docker.com/), when Docker Hub builds new project image, it sends webhook to our autodeploy facility, and autodeploy execute `docker stack deploy -c explorer.yml explorer` for Testnet.

Mainnet autodeploy happens on any push event in `mainnet` branch of mentioned projects, and deploys with `docker stack deploy -c explorer-mainnet explorer-mainnet` command.


## Troubleshooting

1. ssh on `explorer` or `explorer-mainnet` with your credentials (reference with [inventory](../inventory/host) for hosts information)

2. Execute `docker container ps -a` to see which containers is executed now and which are exited

3. Execute `docker container logs -f --tail 100 <CONTAINER_ID>` to figure out container's logs. Choose `CONTAINER_ID` from previous step

4, Execute `docker container stop <CONTAINER_ID>` to stop stucked container. Docker Swarm automatically start another container to fits stack definition needs
