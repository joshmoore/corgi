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

import re
import logging
import github

from config import config


logger = logging.getLogger('corgi.github.impl')

HEADER = '### Referenced Issues:'


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


def update_pr_description(pullrequest, issues, titles):
    logger.info(
        'Updating PR description for %s PR %s' %
            (pullrequest.base.repo.full_name, pullrequest.number)
    )
    body = pullrequest.body
    links = list()
    for issue in issues:
        link = '* [Issue %s: %s](%sissues/%s)' % (
            issue, titles[issue], config['redmine.url'], issue
        )
        links.append(link)
    links = '\n'.join(links)

    lines = [line.strip() for line in body.split('\n')]
    if HEADER in lines:
        logger.info('Found existing list of issues, updating')
        # update existing list
        pos = lines.index(HEADER) + 1
        while pos < len(lines) and lines[pos].startswith('* '):
            del lines[pos]
        if links:
            lines.insert(pos, links)
        else:
            logger.info('Removing existing list of issues')
            del lines[pos - 1]
    elif links:
        logger.info('No existing list of issues found, creating')
        lines.append(HEADER)
        lines.append(links)

    updated_body = '\n'.join(lines)

    if updated_body != body:
        logger.info('Committing new body')
        if not config.get('dry-run'):
            pullrequest.edit(body=updated_body)
    else:
        logger.info('Body unchanged, skipping commit')

    return updated_body
