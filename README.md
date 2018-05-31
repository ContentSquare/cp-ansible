Ansible playbooks for installing the [Confluent Platform](http://www.confluent.io).

Note:
These playbooks are provided without support and are intended to be a guideline. Any issues encountered can be reported
via GitHub issues and will be addressed on a best effort basis.

# Requirements

* Confluent Platform 4.1 or higher
* Ansible 2.4.x or higher

# Introduction

Ansible provides a simple way to deploy, manage, and configure the Confluent Platform services. This repository provides playbooks and templates to easily 
spin up a Confluent Platform installation. Specifically this repository:

* Installs Confluent Platform packages
* Starts services using systemd scripts
* Provides configuration options for plaintext, SSL, and SASL_SSL communication amongst the services

The services that can be installed from this repository are:

* ZooKeeper
* Kafka
* Schema Registry
* REST Proxy
* Confluent Control Center
* Kafka Connect (distributed mode)

Both Enterprise and OSS a available

# Basic usage

```yaml
- hosts: brokers
  gather_facts: no
  vars:
    - hosts:
        zookeepers: "{{ groups['zookeepers'] }}"
        kafka:
          brokers: "{{ groups['brokers'] }}"
        schema:
          registries: "{{ groups['brokers'] }}"
    - confluent_roles:
      - kafka-broker
    - confluent:
        version:
          major: 4
          minor: 1
          patch: 1-1
        oss: yes
        latest: no
    - kafka:
        broker:
          zookeeper_chroot_path: "kafka-cluster1"
        datadir:
          - /kafka_data
  roles:
    - role: contentsquare.confluent-platform
  tags:
    - brokers

```
