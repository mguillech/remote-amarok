# -*- coding: utf-8 -*-

import android
import urllib2
import time

try:
    from urllib.parse import urlencode
except ImportError: # Python 2.7.x running
    from urllib import urlencode

URL = 'http://DJANGO-SERVER/api/run-command/?'
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
            body = msg['body'].lower().split()
            msg_id = int(msg['_id'])
            if body and body[0] == 'amarok':
                print('Amarok command received!')
                print('Running remote command: %s' % ' '.join(body))
                _ = urllib2.urlopen(URL + urlencode({'command': ' '.join(body)}))
                print('Marking message with id %d as read' % msg_id)
                droid.smsMarkMessageRead([msg_id], 1)
                # try not to hang the UI
                time.sleep(5)
