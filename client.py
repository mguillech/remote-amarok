#!/usr/bin/env python

# Copyright (c) Twisted Matrix Laboratories.
# See LICENSE for details.

from twisted.internet.protocol import ClientFactory
from twisted.protocols.basic import LineReceiver
from twisted.internet import reactor
from twisted.python import log
import sys


class RemoteAmarokClient(LineReceiver):
    end = 'quit'

    def lineReceived(self, line):
        print "Remote:", line
        if line==self.end:
            self.transport.loseConnection()

    def connectionMade(self):
        print 'Connected!'
        self.mainLoop()

    def mainLoop(self):
        cmd = raw_input('Command: ')
        self.sendLine(cmd.strip())
        reactor.callLater(.1, self.mainLoop)


class RemoteAmarokClientFactory(ClientFactory):
    protocol = RemoteAmarokClient

    def clientConnectionFailed(self, connector, reason):
        print 'connection failed:', reason.getErrorMessage()
        reactor.stop()

    def clientConnectionLost(self, connector, reason):
        print 'connection lost:', reason.getErrorMessage()
        reactor.stop()


def main():
    factory = RemoteAmarokClientFactory()
    reactor.connectTCP(server, 8000, factory)
    reactor.run()

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print "Usage: %s SERVER" % sys.argv[0]
        sys.exit(1)
    server = sys.argv[1]
    main()
