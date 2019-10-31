Ergoplatform Infrastructure Overview
====================================

This document describes basics about Ergoplatform Infrastructure, including used technologies, services, also that repository design and structure.


## Basics

### Hosting

Ergoplatform infrastructure build upon **Digital Ocean** virtual machines. Create, remove, pause and resume that machines are possible from administration panel and via API. The access to that resources is under @catena2w control as billing. Normal virtual machine status is `Running`.


### Hosts

All mentioned above virtual machines has an IP address and SSH installed, and managed manually (rear case), via Jenkins (sometimes) and via [Ansible](https://docs.ansible.com/ansible/latest/index.html) (usual). In fact, that repository is following [Ansible Best Practices](https://docs.ansible.com/ansible/latest/user_guide/playbooks_best_practices.html) guidelines as that would be shown later.

The actual hosts list is in [Ansible inventory file](../inventory/hosts). Please refer to it for any host IP, host group and name information.

The information specific for hosts are placed in `inventory/host_vars` directory, specific for host groups in `inventory/group_vars`. Variables from groups and hosts are merged together for specific host.

You can monitor hosts CPU load, memory consumption and other system parameters: [Overall hosts statistics](https://grafana.ergoplatform.com/d/M-Xtpr5mz/overall)


### Repository structure

Directories and files structure in this repository is typical for Ansible repos (see [Ansible Best Practices](https://docs.ansible.com/ansible/latest/user_guide/playbooks_best_practices.html)), excluding `/docs` and `/files`. Here is little intro:

- `/docs` used for documentation like this one

- `/files` contains arbitrary files like software configuration, Docker Swarm stacks definitions, some scripts and other important stuff.

    - `/files/configs`: software configuration files and templates
    - `/files/stacks`: Docker Swarm stacks definitions
    - `/files/scipts`: arbitrary useful scripts, for any purpose (including Jenkins jobs)
    - other directories inside `/files` may be temporary, or deprecated, or experimental, anyway, their goal should be clear and depends from current needs.


### Docker Swarm cluster

There is Docker Swarm cluster on some nodes (see `docker-swarm` host group in [inventory](../inventory/hosts)). Docker Swarm hosts any software, needed for crew and community, like Nginx, Jenkins, Grafana and so on.


### Jenkins and CI/CD

Mainnet and Testnet hosts are added to Jenkins and new Ergo node builds automatically and manually deployed on that nodes to corresponding networks.


### Monitoring

The [InfluxDB](https://github.com/influxdata/influxdb) used to store monitoring parameters and statistics.

[Telegraf](https://github.com/influxdata/telegraf) is used to grab metrics from hosts and services and deliver them into InfluxDB.

[Kapacitor](https://github.com/influxdata/kapacitor) is used to analyze metrics and produce alerting.

[node-info-monitor](https://github.com/ergoplatform/node-info-monitor) tool used to grab metrics from Ergo nodes and deliver them into InfluxDB. 

[Grafana](https://github.com/grafana/grafana) is used as monitoring frontend. There are some monitoring dashboards in Grafana:

- [Overall hosts statistics](https://grafana.ergoplatform.com/d/M-Xtpr5mz/overall)
- [Mainnet](https://grafana.ergoplatform.com/d/OwXtQiNZz)
- [Testnet](https://grafana.ergoplatform.com/d/000000001)
