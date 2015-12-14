#!/bin/bash -e
if [ "$1" == "start" ]
then
	if [ -f "/tmp/daemon.pid" ];
	then
		echo "Already running"
	else
		uwsgi_python34 --daemonize /tmp/daemon.pid --ini uwsgi.ini
	fi
elif [ $1 == "stop" ];
then
	pkill uwsgi_python34 -9
	rm /tmp/daemon.pid
else
echo "use start/stop"
fi
