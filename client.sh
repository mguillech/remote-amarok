#!/bin/bash

REMOTE_AMAROK_DIR=$(dirname $0)
python ${REMOTE_AMAROK_DIR}/remote_amarok/client.py $@
