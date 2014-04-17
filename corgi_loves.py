#!/usr/bin/python
# -*- coding: utf-8 -*-

"""

:author: Sam Hart <sam@glencoesoftware.com>

Glue between Github issues and Redmine
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

from logging import StreamHandler
from logging.handlers import WatchedFileHandler

import tornado
import tornado.web

import simplejson
import logging

from blinker import signal


INITIALIZED = signal("corgi:init")


class AbstractException(Exception):
    """
    To be thrown be implementations which are
    solely useful in the class hierarchy.
    """
    pass


class Corgi(object):
    """
    Friend and companion
    """

    def __init__(self):

        try:
            name = self.name()
        except:
            name = "base"

        self.methods = dict()
        self.stack = []
        self.logger = logging.getLogger("corgi.%s" % name)
        self.logger.info("Waiting on initialization")
        INITIALIZED.connect(self.initialize)

    def name(self):
        return self.__class__.__name__

    def initialize(self, sender, paths=None, **kwargs):
        if paths is None:
            self.logger.warn("Paths None")
        self.config = kwargs.get("config", {})
        if not self.config:
            self.logger.warn("No config found")
        self.logger.info("Initialization done")

    def lookup(self, key, prefix=None, safe=True):

        if prefix is None:
            prefix = self.name()
        key = "%s.%s" % (prefix, key)

        value = None
        if safe:
            if self.config:
                value = self.config.get(key, None)
        else:
            value = self.config[key]
        self.logger.debug("config[%s]=%s", key, value)
        return value

    def new_handler(self, signal):

        class EventHandler(tornado.web.RequestHandler):

            def post(self):
                data = simplejson.loads(self.request.body)
                signal.send("server", data=data)

        return EventHandler

    def register(self, sig, paths=None):
        name = sig.name
        if name in self.methods:
            raise Exception("Already registered")

        def method(sender, **kwargs):
            if sender == self.name():
                # Skip own messages
                return
            elif self in self.stack:
                self.logger.warn("Recursive!")
            else:
                self.stack.append(self)
                self.receive(sender, sig=sig, **kwargs)

        self.methods[name] = method
        sig.connect(method)

        # If we've been provided paths for mounting
        # then add a handler.
        if paths is not None:
            paths[r"/event/%s" % self.name()] = self.new_handler(sig)

    def receive(self, sender, **kwargs):
        raise Exception("must be implemented!")


def bark_corgi_bark(config):
    """
    Set up our log level based on the configuration
    availalbe in the cfg file.
    """
    try:
        filename = config['server.logging_filename']
        handler = WatchedFileHandler(filename)
    except KeyError:
        handler = StreamHandler()
    handler.setFormatter(logging.Formatter(config['server.logging_format']))
    root_logger = logging.getLogger('')
    root_logger.setLevel(int(config['server.logging_level']))
    root_logger.addHandler(handler)


def find_the_corgis(names, debug=False):
    """
    Use the names provided in the config to
    search for modules which match the corgi_loves
    requirements:

      * package = 'corgi_loves_$NAME'
      * module = 'handler'
      * classes of type 'corgi_loves.Corgi'

    """
    logger = logging.getLogger("corgi.find")
    instances = []
    for name in names:
        try:
            modname = "corgi_loves_%s.handler" % name
            mod = __import__(modname, "handler")
            for objname in dir(mod.handler):
                try:
                    obj = getattr(mod.handler, objname)
                    if issubclass(obj, Corgi) and obj != Corgi:
                        instances.append(obj())
                except AbstractException:
                    continue
                except AttributeError:
                    continue
                except TypeError:
                    continue
        except:
            logger.error('No corgi handler found: ' + modname,
                         exc_info=debug)
    return instances


def get_em_ready(config):
    """
    Allows each app to register itself at a
    particular sub-url with a single signal
    handler. See the on_init methods for more
    information.
    """
    logger = logging.getLogger("corgi.register")
    paths = dict()
    signal("corgi:init").send("server", paths=paths, config=config)
    paths = paths.items()
    for k, v in paths:
        logger.info("Registered %s", k)
    return paths
