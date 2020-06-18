#!/usr/bin/env bash
exec 2>&1 >/usr/local/logs/doraemon.log

[ -d /usr/local/logs/piptmp ] && rm -rf /usr/local/logs/piptmp
mkdir /usr/local/logs/piptmp
pip install --user --build /usr/local/logs/piptmp -U doraemon -i http://10.169.0.238:5080/simple  --trusted-host 10.169.0.238
rm -rf /usr/local/logs/piptmp
