#!/usr/bin/env python

# Copyright (c) Twisted Matrix Laboratories.
# See LICENSE for details.

import sys
import dbus

from twisted.internet.protocol import ServerFactory
from twisted.protocols.basic import LineReceiver
from twisted.internet import reactor, threads
from twisted.internet.defer import Deferred
from twisted.python import log


AM_COMMANDS = {
        'play': 'Play',
        'stop': 'Stop',
        'pause': 'Pause',
        'next': 'Next',
        'previous': 'Prev',
        'mute': 'Mute',
        'metadata': 'GetMetadata'
        }

def run_amarok_cmd(cmd):
    am = dbus.SessionBus().get_object('org.kde.amarok','/Player')
    dbus_meth = AM_COMMANDS.get(cmd, None)
    if dbus_meth:
        run_meth = getattr(am, dbus_meth)()
        am.ShowOSD()
        return run_meth


class RemoteAmarokServer(LineReceiver):
    end = 'quit'

    def __init__(self):
        self.d = None

    def connectionMade(self):
        self.client_ip = self.transport.getPeer()
        log.msg('Connection from: %s' % self.client_ip)
        self.createDeferred()

    def lineReceived(self, line):
        log.msg('Line received from: %s - %s' % (self.client_ip, line))
        self.d.callback(line)

    def process_received(self, data):
        print 'Processing received:', data
        if data:
            if data == self.end:
                print 'Quit'
                self.transport.loseConnection()
                return
            if data in AM_COMMANDS:
                d = threads.deferToThread(run_amarok_cmd, data)
                d.addCallback(self.send_result)
            else:
                log.msg('Error in cmd: %s' % data)
                self.sendLine('Error: No such command \'%s\'' % data)
        self.createDeferred()

    def send_result(self, result):
        if result:
            self.sendLine(str(result))

    def err_handler(self, failure):
        failure.trap(AttributeError)

    def createDeferred(self):
        self.d = Deferred()
        self.d.addCallbacks(
                self.process_received, self.err_handler)


def main():
    log.startLogging(sys.stdout)
    f = ServerFactory()
    f.protocol = RemoteAmarokServer
    reactor.listenTCP(8000, f)
    reactor.run()

if __name__ == '__main__':
    main()
