#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

:author: Josh Moore <josh@glencoesoftware.com>

Glue between Github issues and Redmine
Copyright (C) 2014 Glencoe Software, Inc.
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

from blinker import signal
from corgi_loves import AbstractException
from corgi_loves import Corgi as Base


RECEIVE_DATA = signal("corgi.ex.data")
OTHER_EXAMPLES = signal("corgi.ex.other")


class Common(Base):

    def __init__(self):
        if self.__class__ == Common:
            raise AbstractException("abstract")
        super(Common, self).__init__()
        self.register(OTHER_EXAMPLES)

    def initialize(self, sender, paths=None, **kwargs):
        super(Common, self).initialize(sender, paths=paths, **kwargs)
        self.register(RECEIVE_DATA, paths=paths)

    def receive(self, sender, sig=None, **kwargs):
        if sig is RECEIVE_DATA:
            self.logger.info("<--%s", sender)
            OTHER_EXAMPLES.send(self.name(), **kwargs)


class Example1(Common):

    def name(self):
        return "example1"


class Example2(Common):

    def name(self):
        return "example2"
