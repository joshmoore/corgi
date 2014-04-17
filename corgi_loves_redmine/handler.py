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
from corgi_loves import Corgi as Base


GET_ISSUE_TITLES = signal("corgi.rm.issue_titles")


class Corgi(Base):

    def __init__(self):
        PULL_REQUEST = signal("corgi.gh.pr")
        super(Corgi, self).__init__()
        self.register(PULL_REQUEST)
        self.register(GET_ISSUE_TITLES)

    def name(self):
        return "redmine"

    def receive(self, sender, sig=None, **kwargs):
        PULL_REQUEST = signal("corgi.gh.pr")
        issues = kwargs.get("issues", [])
        if sig == GET_ISSUE_TITLES:
            from corgi_loves_redmine.impl import get_issue_titles
            titles = kwargs.get("titles", [])
            titles.extend(get_issue_titles(issues))
        elif sig == PULL_REQUEST:
            from corgi_loves_redmine.impl import update_redmine_issues
            data = kwargs.get("data", None)
            pullrequest = kwargs.get("pullrequest", None)
            commits = kwargs.get("commits", None)
            update_redmine_issues(pullrequest, commits, issues, data)

