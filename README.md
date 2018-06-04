## Ansible for Ergoplatform

This is the Ansible repository for Ergoplatform infrastructure management.


## Installation and usage

Checkout from repository:

    git pull git@github.com:ergoplatform/ansible.git
    cd ansible

Install git submodules:

    git submodule add git@github.com:andyceo/ansible-role-docker.git roles/andyceo.docker
    git submodule add git@github.com:andyceo/ansible-role-preconf.git roles/andyceo.preconf
    git submodule add git@github.com:andyceo/ansible-role-users.git roles/andyceo.users
    git submodule add git@github.com:andyceo/ansible-role-ntp.git roles/andyceo.ntp
    git submodule add git@github.com:andyceo/ansible-role-configurator.git roles/andyceo.configurator
    git submodule add git@github.com:andyceo/ansible-role-telegraf.git roles/andyceo.telegraf
    git submodule add git@github.com:andyceo/ansible-role-mailutils.git roles/andyceo.mailutils
    git submodule add git@github.com:andyceo/ansible-role-git.git roles/andyceo.git

Execute playbook `servers.yml`:

    ansible-playbook servers.yml


## Services

- [Jenkins](https://jenkins.ergoplatform.com/) - CI system
- [Grafana](https://grafana.ergoplatform.com/) - monitoring dashboard
- [Portainer](https://portainer.ergoplatform.com/) - Docker Swarm visualization & management


## Get Let's Encrypt certificate with Certbot docker image

docker run -it --rm --name certbot \
      -v infrastructure_certbot-etc:/etc/letsencrypt:rw \
      -v infrastructure_certbot-lib:/var/lib/letsencrypt:rw \
      -v infrastructure_certbot-log:/var/log/letsencrypt:rw \
      -v infrastructure_certbot-webroot:/letsencrypt-webroot:rw \
      certbot/certbot certonly --no-self-upgrade --agree-tos --text
      --non-interactive --keep-until-expiring --expand --webroot --email YOUR@EMAIL.COM \
      -w /letsencrypt-webroot -d EXAMPLE.COM
