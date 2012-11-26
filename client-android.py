# -*- coding: utf-8 -*-

import android
import urllib2
import time

URL = 'http://ra-web.valetin/api/run-command/?command=%s'
droid = android.Android()

command = u''

print('Waiting for commands to arrive...')

while command != u'exitclient':
    msgs = droid.smsGetMessages(True)
    if msgs:
        try:
            msg = msgs.result[0]
        except IndexError:
            pass
        else:
            body = msg['body'].lower()
            msg_id = int(msg['_id'])
            if body.startswith('amarok'):
                print('Message gotten!')
                command = ' '.join(body.split()[1:])
                print('Running remote command: %s' % command)
                _ = urllib2.urlopen(URL % command)
                print('Marking message with id %d as read' % msg_id)
                droid.smsMarkMessageRead([msg_id], 1)
                # try not to hang the UI
                time.sleep(5)

