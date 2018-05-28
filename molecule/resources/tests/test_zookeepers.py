import os
import re

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('zookeepers')

str_reg = r"^server\.(\d+)=([\w\d\-\.]+):(\d+):(\d+)$"
reg = re.compile(str_reg)


def test_zookeeper_listen(host):
    assert host.socket("tcp://0.0.0.0:2181").is_listening


def match_it(x):
    return reg.findall(x)


def test_configuration_vs_myid(host):
    fmyid = host.file('/var/lib/zookeeper/myid').content_string
    fconf = host.file('/etc/kafka/zookeeper.properties').content_string
    hostname = host.ansible.get_variables()['inventory_hostname']
    servers = [match_it(x)[0] for x in fconf.split('\n') if x.startswith('server')]
    servers = [x for x in servers if x[1] == hostname]

    assert len(servers) == 1
    assert servers[0][0] == fmyid


def test_user_group(host):

    assert host.group('confluent').exists
    assert host.user('cp-kafka').exists
    assert "confluent" in host.user('cp-kafka').groups


def test_packages(host):
    package = host.package('confluent-platform-2.11')
    assert package.is_installed


def test_services(host):
    service_name = 'confluent-zookeeper'
    service = host.service(service_name)
    assert service.is_running
    # assert service.is_enabled


def test_zookeeper(host):
    # Send stat and check mode
    mode = host.run("echo stat | nc localhost 2181 | grep Mode | awk '{ print $2 }'")
    assert mode.stdout.strip() == 'standalone'
