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


import config

from corgi_loves import Corgi as Base
from jenkinsapi import Jenkins


def run_jenkins_job(job):
    jenkins = Jenkins(config['jenkins.url'],
                      username=config['jenkins.username'],
                      password=config['jenkins.password'])
    if job in jenkins:
        logging.debug('Invoking Jenkins job %s' % job)
        if not config.get('dry-run'):
            jenkins[job].invoke()
    else:
        logging.error('Jenkins job %s not found' % job)
        logging.debug('Available Jenkins jobs: %s' % ', ' % jenkins.keys())


class Corgi(Base):

    def handle(self, data):

        # Trigger jenkins jobs
        jobs = config.get(
            'repository.mapping.%s:%s' % (
                data['repository']['full_name'],
                data['pull_request']['base']['ref']
            )
        )

        if not jobs:
            jobs = config.get(
                'repository.mapping.%s' % data['repository']['full_name']
            )

        if jobs:
            if isinstance(jobs, list):
                for job in jobs:
                    run_jenkins_job(job)
            else:
                run_jenkins_job(jobs)
        else:
            logging.info("No Jenkins job mappings found")
