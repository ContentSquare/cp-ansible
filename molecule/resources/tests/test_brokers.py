import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('brokers')

zookeeper_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('zookeepers')


def fetch_zookeepers(host):
    config = host.file('/etc/kafka/server.properties').content_string
    zookeepers = [key.split('=')[1].rstrip().split(',') for key in config.split('\n') if key.startswith('zookeeper.connect=')][0]
    return zookeepers[0]


def test_kafka_listen(host):
    assert host.socket("tcp://0.0.0.0:9092").is_listening


def test_my_id(host):
    brokerid = int(host.ansible.get_variables()['kafka']['broker']['id'])
    fconf = host.file('/etc/kafka/server.properties').content_string
    conf_id = int([x.split('=')[1] for x in fconf.split('\n') if x.startswith('broker.id')][0])
    assert brokerid == conf_id


def test_topics(host):
    status = host.run("kafka-topics --zookeeper {} --list".format(fetch_zookeepers(host)))
    assert status.rc == 0


def test_user_group(host):

    assert host.group('confluent').exists
    assert host.user('cp-kafka').exists
    assert "confluent" in host.user('cp-kafka').groups


def test_packages(host):
    package = host.package('confluent-platform-2.11')
    assert package.is_installed


def test_services(host):
    service_name = 'confluent-kafka'
    service = host.service(service_name)
    assert service.is_running
    assert service.is_enabled


