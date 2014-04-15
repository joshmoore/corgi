#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

Copyright (C) 2013 Glencoe Software, Inc.
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer.
2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

"""

import sys
import simplejson
import logging

import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.template

from blinker import signal

from corgi_loves import AbstractException
from corgi_loves import Corgi
from corgi_loves import INITIALIZED
from corgi_loves import RECEIVE_DATA

from config import config

from logging import StreamHandler
from logging.handlers import WatchedFileHandler

logger = logging.getLogger('server')


class EventHandler(tornado.web.RequestHandler):

    def post(self):
        data = simplejson.loads(self.request.body)
        RECEIVE_DATA.send("server", **data)


def main():
    # Set up our log level
    try:
        filename = config['server.logging_filename']
        handler = WatchedFileHandler(filename)
    except KeyError:
        handler = StreamHandler()
    handler.setFormatter(logging.Formatter(config['server.logging_format']))
    root_logger = logging.getLogger('')
    root_logger.setLevel(int(config['server.logging_level']))
    root_logger.addHandler(handler)

    settings = {
    }

    if 'debug' in config:
        logger.info('Enabling Tornado Web debug mode')
        settings['debug'] = config['debug']

    host = config['server.socket_host']
    port = int(config['server.socket_port'])

    handlers = config['server.handlers']
    for handler in handlers:
        try:
            modname = "corgi_loves_%s.handler" % handler
            mod = __import__(modname, "handler")
            for objname in dir(mod.handler):
                try:
                    obj = getattr(mod.handler, objname)
                    if issubclass(obj, Corgi) and obj != Corgi:
                        corgi = obj()
                except AbstractException:
                    continue
                except AttributeError:
                    continue
                except TypeError:
                    continue
        except:
            logger.error('No corgi handler found: ' + modname,
                      exc_info=('debug' in config))

    INITIALIZED.send("server", message="ready")

    application = tornado.web.Application([
        (r"/event", EventHandler),
    ], **settings)

    if config.get('dry-run'):
        logger.info('In dry-run mode')

    logger.info('Starting corgi server http://%s:%d/' % (host, port))
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(port, host)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)
