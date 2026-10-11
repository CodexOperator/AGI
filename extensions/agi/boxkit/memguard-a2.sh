#!/bin/sh
# A2 -- ENABLE + START (box-wide live behaviour: from the first tick every agi-post@ spine/harness is set to -900 / nice -5)
set -eu
[ -e /usr/local/sbin/agi-memguard.py ] && [ -e /etc/systemd/system/agi-memguard.service ] || { echo "A2 REFUSED: A1 has not run"; exit 1; }
sudo -n systemctl enable --now agi-memguard.service
