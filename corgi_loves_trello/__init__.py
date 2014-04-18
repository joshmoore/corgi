#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

:author: Josh Moore <josh@glencoesoftware.com>

Trello Handler API

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

from corgi_loves import Corgi
from blinker import signal

PULL_REQUEST = signal("corgi:gh:pr")


class trello(Corgi):

    def __init__(self):
        super(trello, self).__init__()

    def on_init(self, sender, paths=None, **kwargs):
        self.mount_at_path(DATA, paths)
        self.register(PULL_REQUEST)

    def receive(self, sender, sig=None, data=None, **kwargs):
        if sig is PULL_REQUEST:
            pr_id = kwargs.get("pr_id", "unknown")
            self.logger.info("Received PR %s", pr_id)
            self.handle_pr(pr_id)

    def handle_pr(self, pr_id):
        board = self.get_pr_board()
        card = self.find_pr_card(board)

    def get_pr_board(self):
        board_url = self.lookup("pr_board_url")
        return board_url

    def find_pr_card(self, board):
        pass
