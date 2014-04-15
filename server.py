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

import simplejson
import logging
import re
import os

import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.template

from blinker import signal

from corgi import Corgi
from corgi import InitializedSignal

from config import config
from collections import defaultdict

from logging import StreamHandler
from logging.handlers import WatchedFileHandler

log = logging.getLogger('server')


def get_pullrequest(repo_name, pr_number):
    gh = github.Github(config['git.token'])
    repo = gh.get_repo(repo_name)
    return repo.get_pull(pr_number)


def get_commits_from_pr(pullrequest):
    cached = getattr(pullrequest, '_cached_commits', None)
    if not cached:
        cached = pullrequest.get_commits()
        setattr(pullrequest, '_cached_commits', cached)
    return cached


def get_issues_from_pr(pullrequest):
    text = [pullrequest.title, pullrequest.body]
    for commit in get_commits_from_pr(pullrequest):
        text.append(commit.commit.message)
    return sorted(set(map(int, re.findall(r'\bgs-(\d+)', ' '.join(text)))))


def get_issue_titles(issues):
    corgi = Corgi(config['redmine.url'], config['redmine.auth_key'])
    titles = dict()
    if corgi.connected:
        for issue in issues:
            titles[issue] = corgi.get_issue_title(issue)
    return titles


class EventHandler(tornado.web.RequestHandler):

    receive_data = signal('receive_data')

    def initialize(self, **kwargs):
        print kwargs
        self.settings = settings
        self.handlers = dict()
        for k, v in self.settings.items():
            if isinstanceof(v, Corgi):
                self.handlers[k] = v
        logging.info("Running with handlers %s" % ",".join(self.handlers.keys()))

    def post(self):
        data = simplejson.loads(self.request.body)
        receive_data.send(data)


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
        "handlers": {},
    }

    if 'debug' in config:
        log.info('Enabling Tornado Web debug mode')
        settings['debug'] = config['debug']

    host = config['server.socket_host']
    port = int(config['server.socket_port'])

    handlers = config['server.handlers']
    for handler in handlers:
        try:
            modname = "corgi_loves_%s.handler" % handler
            mod = __import__(modname, "handler")
            corgi = getattr(mod.handler, "Corgi")()
        except:
            log.error('No corgi handler found: ' + modname,
                      exc_info=('debug' in config))
            continue
        settings["handlers"][handler] = corgi

    InitializedSignal.send("ready")
    application = tornado.web.Application([
        (r"/event", EventHandler),
    ], settings)

    if config.get('dry-run'):
        log.info('In dry-run mode')

    log.info('Starting corgi server http://%s:%d/' % (host, port))
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(port, host)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()
