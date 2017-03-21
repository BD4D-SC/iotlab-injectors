#!/bon/bash

cat >> $HOME/.ssh/config << EOT
Host a8-*
User root
StrictHostKeyChecking no
UserKnownHostsFile /dev/null

Host a8-*.grenoble.*
ProxyCommand ssh grenoble.iot-lab.info -W node-%h:%p

Host a8-*.saclay.*
ProxyCommand ssh saclay.iot-lab.info -W node-%h:%p
EOT
