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

from corgi_loves import Corgi
from blinker import signal

RECEIVE_DATA = signal("corgi:gh:data")
PULL_REQUEST = signal("corgi:gh:pr")


class github(Corgi):

    def __init__(self):
        super(github, self).__init__()

    def on_init(self, sender, paths=None, **kwargs):
        self.register(RECEIVE_DATA, paths=paths)

    def receive(self, sender, **kwargs):
        data = kwargs.get("data", {})
        self.logger.info(
            "Received event for PR %s" % data['pull_request']['number']
        )

        from impl import get_pullrequest
        from impl import get_commits_from_pr
        from impl import get_issues_from_pr
        from impl import update_pr_description
        GET_ISSUE_TITLES = signal("corgi:rm:issues_titles")

        try:
            pullrequest = get_pullrequest(
                data['repository']['full_name'],
                data['pull_request']['number']
            )

            issues = get_issues_from_pr(pullrequest)
            titles = []
            GET_ISSUE_TITLES.send(self, issues=issues, titles=titles)
            update_pr_description(pullrequest, issues, titles)
            commits = get_commits_from_pr(pullrequest)

            PULL_REQUEST.send("github",
                              pull_request=pullrequest,
                              commits=commits,
                              issues=issues,
                              data=data)
        except:
            self.logger.exception("Exception updating cross-links")

