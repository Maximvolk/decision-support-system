#!/usr/bin/env bash
# wait 30 seconds until elasticsearch and mysql are completely started
sleep 10
echo "waited 10 sec"
sleep 20
echo "waited 30 sec"

# start uwsgi with config from current directory
uwsgi --ini uwsgi.ini
