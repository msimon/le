
# coding: utf-8
# vim: set ts=4 sw=4 et:

__author__ = 'Logentries'

__all__ = ['FormatPlain', 'FormatSyslog']


import datetime
import socket

class FormatPlain(object):

    """Formats lines as plain text, prepends each line with token."""

    def __init__(self, token):
        self._token = token

    def format_line(self, line):
        lines = []
        for l in filter(None, line.split("\n")):
            lines.append(self._token + l)
        return (''.join(x+"\n" for x in lines))


class FormatSyslog(object):

    """Formats lines according to Syslog format RFC 5424. Hostname is taken
    from configuration or current hostname is used."""

    def __init__(self, hostname, appname, token):
        if hostname:
            self._hostname = hostname
        else:
            self._hostname = socket.gethostname()
        self._appname = appname
        self._token = token

    def format_line(self, line, msgid='-', token=''):
        if not token:
            token = self._token
        lines = []
        for l in filter(None, line.split("\n")):
            lines.append(
                '{token}<14>1 {dt}Z {hostname} {appname} - {msgid} - hostname={hostname} appname={appname} {line}'.format(
                    token=token, dt=datetime.datetime.utcnow().isoformat('T'),
                    hostname=self._hostname, appname=self._appname,
                    msgid=msgid, line=l)
            )
        return (''.join(x+"\n" for x in lines))

class FormatFliptop(object):

    """marc@fliptop.com: Formater for fliptop"""

    def __init__(self, hostname, appname, token):
        if hostname:
            self._hostname = hostname
        else:
            self._hostname = socket.gethostname()
        self._appname = appname
        self._token = token

    def format_line(self, line, msgid='-', token=''):
        if not token:
            token = self._token

        logs = []
        current_log = ''
        for l in filter(None, line.split("\n")):
            if token:
                lt = "token=" + token + " " + l
            else:
                lt = l
            if l.startswith(" ") or l.startswith("\t"):
                current_log = current_log + lt + "\n"
            else:
                if current_log:
                    logs.append(current_log)
                current_log = lt + "\n"
        if current_log:
            logs.append(current_log)

        ret_logs = []
        for log in logs:
            log = log.rstrip();
            if self._hostname or self._appname:
                log = log + " --"
            if self._hostname:
                log = log + " hostname=" + self._hostname
            if self._appname:
                log = log + " appname=" + self._appname
            ret_logs.append(log + "\n")

        return ''.join(x for x in ret_logs)
