[![Build Status](https://travis-ci.org/ContentSquare/cp-ansible.svg?branch=master)](https://travis-ci.org/ContentSquare/cp-ansible)

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
    - hosts_zookeepers: "{{ groups['zookeepers'] }}"
    - hosts_kafka_brokers: "{{ groups['brokers'] }}"
    - hosts_schema_registries: "{{ groups['brokers'] }}"
    - confluent_roles:
      - kafka-broker
    - confluent_version: 4.1.1-1
    - confluent_oss: yes
    - confluent_latest: no
    - kafka_broker_zookeeper_chroot_path: "kafka-cluster1"
    - kafka_datadir:
          - /kafka_data
  roles:
    - role: contentsquare.confluent-platform
  tags:
    - brokers

```
