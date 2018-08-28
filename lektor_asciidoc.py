# -*- coding: utf-8 -*-
import sys
from subprocess import PIPE, Popen

from lektor.pluginsystem import Plugin
from lektor.types import Type


def asciidoc_to_html(text):
    p = Popen(['asciidoctor', '-s','-'],
              stdin=PIPE, stdout=PIPE, stderr=PIPE)
    if sys.version_info[0] < 3:
        out, err = p.communicate(text)
    else:
        out, err = p.communicate(text.encode('utf-8'))

    if p.returncode !=  0:
        raise RuntimeError('asciidoctor: "%s"' % err)

    return out


# Wrapper with an __html__ method prevents Lektor from escaping HTML tags.
class HTML(object):
    def __init__(self, html):
        self.html = html

    def __html__(self):
        return self.html


class AsciiDocType(Type):
    widget = 'multiline-text'

    def value_from_raw(self, raw):
        if sys.version_info[0] < 3:
            return HTML(asciidoc_to_html(raw.value or u''))
        else:
            return HTML(asciidoc_to_html(raw.value or u'').decode('utf-8'))


class AsciiDocPlugin(Plugin):
    name = u'AsciiDoc'
    description = u'Adds AsciiDoc field type to Lektor.'

    def on_setup_env(self, **extra):
        self.env.add_type(AsciiDocType)
