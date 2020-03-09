#!/usr/bin/env python3
"""Nele - Generate fancy newsletters with markdown

Usage:
  nele [--config <FILE>] draft <newsletter_source> [<recipient>]
  nele [--config <FILE>] send <newsletter_source>
  nele (-h | --help)
  nele --version

Options:
  --version           Show version.
  -h --help           Show this screen.
  -c --config <FILE>  Configuration File [default: nele.yml]

"""

___version___ = '0.4.0'

import smtplib
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
import email.utils

import mimetypes
import getpass
import os
import sys
import sqlite3

from docopt import docopt
import yaml
import frontmatter
import markdown
from mdx_gfm import GithubFlavoredMarkdownExtension
from jinja2 import Template


def setup_smtp(config):
    if config['sender'].get('ssl', False):
        smtp = smtplib.SMTP_SSL(config['sender']['host'], config['sender'].get('port', 993))
    else:
        smtp = smtplib.SMTP(config['sender']['host'], config['sender'].get('port', 587))

    if config['sender'].get('starttls', False):
        smtp.starttls()

    smtp.login(config['sender']['user'], getpass.getpass(f"SMTP password for user {config['sender']['user']}: "))
    return smtp


def load_recipients(config):

    if config['source']['provider'] == 'inline':
        recipients = config['source']['recipients']
        if not len(recipients):
            print('No inline recipients configured', file=sys.stderr)
            exit(2)
        return recipients

    if config['source']['provider'] != 'sqlite':
        print('currently, only sqlite is supported', file=sys.stderr)
        exit(1)

    conn = sqlite3.connect(config['source']['url'])
    c = conn.cursor()
    recipients = []
    rows = c.execute(config['source']['query'])
    titles = [x[0] for x in c.description]
    for row in rows:
        recipient = {}
        for idx in range(len(titles)):
            recipient[titles[idx]] = row[idx]
        recipients.append(recipient)
    conn.close()

    return recipients


def send_newsletter(source, config, recipients):
    smtp = setup_smtp(config)

    # Load E-Mail contents
    post = frontmatter.load(source)

    # Load markdown parser
    md = markdown.Markdown(extensions=[GithubFlavoredMarkdownExtension()])

    with open(config['email']['template'], 'r') as f:
        html_template = Template(f.read())

    markdown_template = Template(post.content)

    for receiver in recipients:
        msg = MIMEMultipart('mixed')
        msg['Subject'] = post['subject']
        msg['From'] = config['sender']['sender']
        msg['To'] = receiver['email']
        msg['Date'] = email.utils.formatdate()
        msg['Message-ID'] = email.utils.make_msgid()
        msg.preamble = post['subject']

        context = receiver.copy()
        context.update(post)
        plain = markdown_template.render(**context)

        context['content'] = md.convert(plain)
        html = html_template.render(**context)
        textmsg = MIMEMultipart('alternative')
        textmsg.attach(MIMEText(plain, 'plain', 'utf-8'))
        textmsg.attach(MIMEText(html, 'html', 'utf-8'))
        msg.attach(textmsg)

        for fname in post.get('attachments', []):
            fname = os.path.join(os.path.dirname(source), fname)
            attachment = MIMEApplication(open(fname, 'rb').read())
            attachment.add_header('Content-Type', mimetypes.guess_type(fname)[0])
            attachment.add_header('Content-Disposition', 'attachment; filename=%s' %
                                  os.path.basename(fname))
            msg.attach(attachment)

        print('sending email to %s' % receiver['email'])

        smtp.sendmail(config['sender']['sender'], receiver['email'], msg.as_string())

    smtp.quit()


def main():
    arguments = docopt(__doc__, version='Nele %s' % ___version___)
    source = os.path.abspath(arguments['<newsletter_source>'])

    # Work relative to the config file
    config_file = os.path.abspath(arguments['--config'])
    os.chdir(os.path.dirname(config_file))
    config = yaml.safe_load(open(config_file))

    if arguments['send']:
        print('Are you sure you want to send a newsletter to EVERYONE? [y/N]', end=' ')
        if input().lower() != 'y':
            print("aborting....")
            return
        recipients = load_recipients(config)
        send_newsletter(source, config, recipients)
    if arguments['draft']:
        print("Welcome to draft mode!")
        if arguments['<recipient>']:
            config['draft']['email'] = arguments['<recipient>']
        send_newsletter(source, config, [config['draft']])


if __name__ == '__main__':
    main()
