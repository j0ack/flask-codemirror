#! /usr/bin/env python
# -*- coding: utf-8 -*-

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


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
try:
    from urllib.parse import urljoin
except ImportError:
    from urlparse import urljoin


__author__ = 'TROUVERIE Joachim'
__all__ = ['CodeMirror', 'CodeMirrorConfigException']


class CodeMirrorConfigException(Exception):
    pass


class CodeMirrorHeaders(object):
    """CodeMirror extension for Flask
    :param config: Flask app config
    """

    LANGUAGES_KEY = 'CODEMIRROR_LANGUAGES'
    THEME_KEY = 'CODEMIRROR_THEME'
    ADDONS_KEY = 'CODEMIRROR_ADDONS'
    VERSION_KEY = 'CODEMIRROR_VERSION'
    CDN_URL = '//cdnjs.cloudflare.com/ajax/libs/codemirror/{0}/'
    LANGUAGE_REL_URL = 'mode/{0}/{0}.js'
    THEME_REL_URL = 'theme/{0}.css'
    ADDON_REL_URL = 'addon/{0}/{1}.js'
    ADDON_CSS_REL_URL = 'addon/{0}/{1}.css'

    def __init__(self, config):
        # get values from config
        self.theme = config.get(self.__class__.THEME_KEY, None)
        self.languages = config.get(self.__class__.LANGUAGES_KEY, [])
        self.addons = config.get(self.__class__.ADDONS_KEY, None)
        self.version = config.get(self.__class__.VERSION_KEY, '5.61.0')
        # construct base url
        self.base_url = self.__class__.CDN_URL.format(self.version)
        if not self.languages:
            error = '{0} is required'.format(self.__class__.LANGUAGES_KEY)
            raise CodeMirrorConfigException(error)

    def _get_tag(self, url, tag, print_warn=True):
        """Check if url is available and returns given tag type
        :param url: url to content relative to base url
        :param anchor: anchor type to return
        :param print_warn: if True print warn when url is unavailable
        """
        # construct complete url
        complete_url = urljoin(self.base_url, url)
        # check if exists
        if requests.get('http:' + complete_url).ok:
            # construct tag
            if tag == 'script':
                return '<script src="{0}"></script>'.format(complete_url)
            elif tag == 'stylesheet':
                return '<link rel="stylesheet" href="{0}">'.format(complete_url)
            else:
                warnings.warn('Given tag is not valid')
        elif print_warn:
            warnings.warn('Url {0} not valid'.format(complete_url))
        return None

    def include_codemirror(self):
        """Include resources in pages"""
        contents = []
        # base
        js = self._get_tag('codemirror.js', 'script')
        css = self._get_tag('codemirror.css', 'stylesheet')
        if js and css:
            contents.append(js)
            contents.append(css)
        # languages
        for language in self.languages:
            url = self.__class__.LANGUAGE_REL_URL.format(language)
            js = self._get_tag(url, 'script')
            if js:
                contents.append(js)
        # theme
        if self.theme:
            url = self.__class__.THEME_REL_URL.format(self.theme)
            css = self._get_tag(url, 'stylesheet')
            if css:
                contents.append(css)
        # addons
        if self.addons:
            # add to list
            for addon_type, name in self.addons:
                url = self.__class__.ADDON_REL_URL.format(addon_type, name)
                js = self._get_tag(url, 'script')
                if js:
                    contents.append(js)
                # if there is a css file relative to this addon
                url = self.__class__.ADDON_CSS_REL_URL.format(addon_type, name)
                css = self._get_tag(url, 'stylesheet', False)
                if css:
                    contents.append(css)
        # return html
        return Markup('\n'.join(contents))


class CodeMirror(object):
    """CodeMirror Flask extension
    :param app: Flask instance
    """
    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        """Register CodeMirror as a Flask extension
        :param app: Flask instance
        """
        if not hasattr(app, 'extensions'):
            app.extensions = {}
        app.extensions['codemirror'] = CodeMirrorHeaders(app.config)
        app.context_processor(self.context_processor)

    @staticmethod
    def context_processor():
        return {
            'codemirror': current_app.extensions['codemirror']
        }
