#!/bin/sh

REMOTE_HOST=eustis
REMOTE_USER=svig
REMOTE_PORT=20000

COMMAND="ssh -qfN -R ${REMOTE_PORT}:localhost:22 ${REMOTE_USER}@${REMOTE_HOST}"

pgrep -f -x "$COMMAND" > /dev/null 2>&1 || ${COMMAND}

ssh ${REMOTE_USER}@${REMOTE_HOST} netstat -an | egrep "tcp.*:${REMOTE_PORT}.*LISTEN" > /dev/null 2>&1

if [ $? -ne 0 ]; then
	pkill -f -x "$COMMAND"
	$COMMAND
	echo "Restarting connection"
fi
