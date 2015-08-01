
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
