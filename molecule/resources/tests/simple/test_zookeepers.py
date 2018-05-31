import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('zookeepers')

def test_zookeeper(host):
    # Send stat and check mode
    mode = host.run("echo stat | nc localhost 2181 | grep Mode | awk '{ print $2 }'")
    assert mode.stdout.strip() == 'standalone'
