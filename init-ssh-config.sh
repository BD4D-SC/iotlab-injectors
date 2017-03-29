#!/bin/bash

cat >> $HOME/.ssh/config << EOT
Host a8-*
User root
StrictHostKeyChecking no
UserKnownHostsFile /dev/null
LogLevel ERROR

Host a8-*.grenoble.*
ProxyCommand ssh grenoble.iot-lab.info -W node-%h:%p

Host a8-*.saclay.*
ProxyCommand ssh saclay.iot-lab.info -W node-%h:%p

# prevent ssh-server connections rate-limit issues
Host grenoble.iot-lab.info saclay.iot-lab.info
ControlMaster auto
ControlPersist yes
ControlPath /tmp/ssh_mux_%h_%p_%r
EOT
