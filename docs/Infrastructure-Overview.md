Ergoplatform Infrastructure Overview
====================================

This document describes basics about Ergoplatform Infrastructure, including used technologies, services, also that repository design and structure.


## Basics

### Hosting

Ergoplatform infrastructure build upon **Digital Ocean** virtual machines. Create, remove, pause and resume that machines are possible from administration panel and via API. The access to that resources is under @catena2w control as billing. Normal virtual machine status is `Running`.


### Hosts

All mentioned above virtual machines has an IP address and SSH installed, and managed manually or through [Ansible](https://docs.ansible.com/ansible/latest/index.html). In fact, that repository is following [Ansible Best Practices](https://docs.ansible.com/ansible/latest/user_guide/playbooks_best_practices.html) guidelines as that would be shown later.

The actual hosts list is placed under [hosts](inventory/hosts) Ansible inventory file. Please refer to it for any host IP, role and name information.
