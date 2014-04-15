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

import logging

from blinker import signal

RECEIVE_DATA = "corgi.base.receive-data"

INITIALIZED = "corgi.base.initialized"


class Corgi(object):
    """
    Friend and companion
    """

    def __init__(self):

        try:
            name = self.name()
        except:
            name = "base"

        self.logger = logging.getLogger("corgi.%s" % name)
        signal(RECEIVE_DATA).connect(self.receive_data)
        signal(INITIALIZED).connect(self.initialized)
        self.logger.info("Registered")

    def sender(self, kwargs):
        return kwargs.get("_sender", "unknown")

    def name(self):
        raise Exception("Must be implemented!")

    def initialized(self, kwargs):
        self.logger.info("Ready")

    def receive_data(self, kwargs):
        raise Exception("Must be implemeneted!")
