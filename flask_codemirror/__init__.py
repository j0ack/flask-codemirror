#! /usr/bin/env python
#-*- coding : utf-8 -*-
# vim:set shiftwidth=4 tabstop=4 expandtab textwidth=79:

"""
    Flask-Codemirror
    ~~~~~~~~~~~~~~~~

    Manage a source code field using CodeMirror and WTForms
    for Flask
"""

import requests
import warnings
from jinja2 import Markup
from flask import current_app


__all__ = ['CodeMirror']

class CodeMirrorHeaders(object):
    """
        CodeMirror extension for Flask
        :param : config - app config
    """
    addons        = (('mode','overlay'),)
    languages_key = 'CODEMIRROR_LANGUAGES'
    theme_key     = 'CODEMIRROR_THEME'
    addon_key     = 'CODEMIRROR_ADDONS'
    cdn_url       = 'http://cdnjs.cloudflare.com/ajax/libs/codemirror/'
    mode_url      = cdn_url + '{0}/mode/{1}/{1}.js'
    theme_url     = cdn_url + '{0}/theme/{1}.css'
    addon_url     = cdn_url + '{0}/addon/{1}/{2}.js'
    base_css_url  = cdn_url + '{0}/codemirror.css'
    base_url      = cdn_url + '{0}/codemirror.js'

    def __init__(self, config) :
        self.theme = config.get(self.__class__.theme_key, None)         
        self.languages = config.get(self.__class__.languages_key, None)
        self.extra_addons = config.get(self.__class__.addon_key,None)
        if not self.languages :
            warnings.warn('Flask-Codemirror : {0} ' \
                          'is set to None,'.format(self.__class__.languages_key))


    def include_codemirror(self, version = '4.7.0'):
        """
           Include JavaScript in pages
        """
        content = []
        url = self.__class__.base_url.format(version)
        content.append('<script src = "{0}"></script>'.format(url))
        # languages
        if self.languages:
            for language in self.languages:
                url  = self.__class__.mode_url.format(version, language)
                if requests.get(url).ok:
                    content.append('<script src="{0}"></script>'.format(url))
                else:
                    warnings.warn('Language {0} unavailable'.format(language))
        # theme
        url = self.__class__.base_css_url.format(version)
        content.append('<link rel = "stylesheet" href = "{0}">'.format(url))
        if self.theme:
            url  = self.__class__.theme_url.format(version, self.theme)
            if requests.get(url).ok:
                content.append('<link rel="stylesheet" href="{0}">'.format(url))
            else:
                warnings.warn('Theme {0} not available'.format(self.theme))
        # addons
        if self.extra_addons:
            self.__class__.addons += self.extra_addons
        for addon_type,name in self.__class__.addons:
            url = self.__class__.addon_url.format(version,addon_type,name)
            if requests.get(url).ok:
                content.append('<script src="{0}"></script>'.format(url))
            else:
                warnings.warn('addon at {0} not available'.format(url))

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

