#!/bin/bash

export DISPLAY=:0.0
PID=$(pgrep -u $USER | head -n 1)
declare DBUS_SESSION_BUS_ADDRESS=$(cat /proc/${PID}/environ | tr '\0' '\n' | grep "DBUS_SESSION_BUS_ADDRESS=")
export DBUS_SESSION_BUS_ADDRESS="${DBUS_SESSION_BUS_ADDRESS:25}"
# echo "DBUS_SESSION_BUS_ADDRESS = ${DBUS_SESSION_BUS_ADDRESS}"
REMOTE_AMAROK_DIR=$(dirname $0)
twistd -oy $REMOTE_AMAROK_DIR/server.tac
