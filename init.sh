sed -i 's/#releasever=latest/releasever=latest/g' /etc/yum.conf
yum install gcc libffi-devel python-devel openssl-devel libxml2-devel libxslt-devel -y
pip install -U setuptools
pip install -r requirements.txt
sh  shell/doraemon_install.sh
cd supervisor
sh init.sh