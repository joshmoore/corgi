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
from corgi_loves import Corgi


GET_ISSUE_TITLES = signal("corgi:rm:issue_titles")


class redmine(Corgi):

    def __init__(self):
        PULL_REQUEST = signal("corgi:gh:pr")
        super(redmine, self).__init__()
        self.register(PULL_REQUEST)
        self.register(GET_ISSUE_TITLES)

    def receive(self, sender, sig=None, **kwargs):
        PULL_REQUEST = signal("corgi:gh:pr")
        issues = kwargs.get("issues", [])
        if sig == GET_ISSUE_TITLES:
            titles = kwargs.get("titles", [])
            titles.extend(self.get_issue_titles(issues))
        elif sig == PULL_REQUEST:
            data = kwargs.get("data", None)
            pullrequest = kwargs.get("pullrequest", None)
            commits = kwargs.get("commits", None)
            self.update_redmine_issues(pullrequest, commits, issues, data)

    def create_tree_url(self, data, head_or_base='head'):
        ref = data['pull_request'][head_or_base]['ref']
        url = '%s/tree/%s' % (
            data['pull_request'][head_or_base]['repo']['html_url'],
            ref
        )
        return url

    def make_past_tense(self, verb):
        if not verb.endswith('d'):
            return verb + 'd'
        return verb

    def create_issue_update(self, pullrequest, commits, data):
        return self.render('updated_pull_request.textile',
                           data=data,
                           head_url=self.create_tree_url(data, 'head'),
                           base_url=self.create_tree_url(data, 'base'),
                           make_past_tense=self.make_past_tense,
                           commits=commits,
                           )

    def get_issue_titles(self, issues):
        from corgi_loves_redmine.impl import RedmineConnection
        corgi = RedmineConnection(
            self.config['redmine.url'],
            self.config['redmine.auth_key'])
        titles = dict()
        if corgi.connected:
            for issue in issues:
                titles[issue] = corgi.get_issue_title(issue)
        return titles

    def update_redmine_issues(self, pullrequest, commits, issues, data):
        from corgi_loves_redmine.impl import RedmineConnection
        if not issues:
            self.logger.info("No issues found")
        else:
            self.logger.info(
                "Updating Redmine issues %s" % ", ".join(map(str, issues))
            )

        if issues and not self.config.get('dry-run'):
            c = RedmineConnection(
                self.config['redmine.url'], self.config['redmine.auth_key'],
                self.config.get('user.mapping.%s' % data['sender']['login'])
            )
            if not c.connected:
                self.logger.error("Connection to Redmine failed")
                return

        if data['action'] == 'closed' and data['pull_request']['merged']:
            data['action'] = 'merged'
        status = self.config.get('redmine.status.on-pr-%s' % data['action'])
        update_message = self.create_issue_update(pullrequest, commits, data)
        self.logger.debug(update_message)

        if not self.config.get('dry-run'):
            for issue in issues:
                c.update_issue(issue, update_message, status)
                self.logger.info("Added comment to issue %s" % issue)
