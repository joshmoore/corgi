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

import os
import sys
import logging

import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.template

from corgi_loves import bark_corgi_bark
from corgi_loves import find_the_corgis
from corgi_loves import get_em_ready

from blinker import signal
from config import config

logger = logging.getLogger('server')


def main():

    settings = dict()

    if 'debug' in config:
        logger.info('Enabling Tornado Web debug mode')
        settings['debug'] = config['debug']

    if config.get('dry-run'):
        logger.info('In dry-run mode')

    bark_corgi_bark(config)
    names = config['server.handlers']

    class EventHandler(tornado.web.RequestHandler):

        def get(self):
            t = os.path.join(os.path.dirname(__file__), 'templates')  # TODO
            t = os.path.join(t, "index_info.textile")
            self.render(t, data=list(names))

    pups = find_the_corgis(names, "debug" in config)
    leashes = get_em_ready(pups)
    leashes.append(("/*", EventHandler))
    application = tornado.web.Application(leashes, **settings)

    host = config['server.socket_host']
    port = int(config['server.socket_port'])
    logger.info('Starting corgi server http://%s:%d/' % (host, port))

    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(port, host)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)
