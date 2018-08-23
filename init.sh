sed -i 's/#releasever=latest/releasever=latest/g' /etc/yum.conf
yum install gcc -y
pip install -r requirements.txt
sh  shell/doraemon_install.sh
ln -s /usr/local/redis/bin/redis-server /usr/bin/redis-server
