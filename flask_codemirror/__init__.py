#! /usr/bin/env python
#-*- coding : utf-8 -*-
# vim:set shiftwidth=4 tabstop=4 expandtab textwidth=79:

"""
    Flask-Codemirror
    ~~~~~~~~~~~~~~~~

    Manage a source code field using CodeMirror and WTForms
    for Flask
"""

import urllib2
import warnings
from jinja2 import Markup
from flask import current_app


__all__ = ['CodeMirror']

class CodeMirrorHeaders(object):
    """
        CodeMirror extension for Flask
        :param : config - app config
    """
    languages_key = 'CODEMIRROR_LANGUAGES'
    theme_key     = 'CODEMIRROR_THEME'
    cdn_url       = 'http://cdnjs.cloudflare.com/ajax/libs/codemirror/'
    mode_url      = cdn_url + '{0}/mode/{1}/{1}.js'
    theme_url     = cdn_url + '{0}/theme/{1}.css'
    base_css_url  = cdn_url + '{0}/codemirror.css'
    base_url      = cdn_url + '{0}/codemirror.js'

    def __init__(self, config) :
        self.theme = config.get(self.__class__.theme_key, None)
        # languages              
        self.languages = config.get(self.__class__.languages_key, None)
        if not self.languages :
            warnings.warn('Flask-Codemirror : {0} ' \
                          'is set to None,'.format(self.__class__.languages_key))

    def include_codemirror(self, version = '3.20.0'):
        """
           Include JavaScript in pages
        """
        content = []
        url = self.__class__.base_url.format(version)
        content.append('<script src = "{0}"></script>'.format(url))
        # languages
        if self.languages :
            for language in self.languages :
                try : 
                    url  = self.__class__.mode_url.format(version, language)
                    print type(url)
                    print url
                    html = urllib2.urlopen(url)
                    content.append('<script src="{0}"></script>'.format(url))
                except urllib2.HTTPError :
                    warnings.warn('Language {0} unavailable'.format(language))
        # theme
        url = self.__class__.base_css_url.format(version)
        content.append('<link rel = "stylesheet" href = "{0}">'.format(url))
        if self.theme :
            try :
                url  = self.__class__.theme_url.format(version, self.theme)
                html = urllib2.urlopen(url)
                content.append('<link rel="stylesheet" href="{0}">'.format(url))
            except urllib2.HTTPError :
                warnings.warn('Theme {0} not available'.format(self.theme))
        return Markup('\n'.join(content))

    def html_head(self):
        return self.include_codemirror()

class CodeMirror(object):
    """
        CodeMirror class
        Register CodeMirror as a Flask ext
    """
    def __init__(self, app = None):
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        if not hasattr(app, 'extensions'):
            app.extensions = {}
        app.extensions['codemirror'] = CodeMirrorHeaders(app.config)
        app.context_processor(self.context_processor)

    @staticmethod
    def context_processor():
        return {
            'codemirror': current_app.extensions['codemirror']
        }

