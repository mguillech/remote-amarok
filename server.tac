# -*- coding: utf-8 -*-
#
import os
import sys
from twisted.application import service, internet

sys.path.insert(0, os.path.dirname(__file__))

def getRemoteAmarokService():
    f = ServerFactory()
    f.protocol = RemoteAmarokServer
    return internet.TCPServer(8000, f)


from server import ServerFactory, RemoteAmarokServer

application = service.Application('remote_amarok_server')
am_server_service = getRemoteAmarokService()
am_server_service.setServiceParent(application)

