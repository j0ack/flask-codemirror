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
    Flask Codemirror Test
    ~~~~~~~~~~~~~~~~~~~~~

    Unit tests for Flask-CodeMirror
"""

import unittest

from flask import Flask, render_template_string
from flask.ext.wtf import Form
from flask_codemirror import CodeMirror, CodeMirrorConfigException
from flask_codemirror.fields import CodeMirrorField


__author__ = 'TROUVERIE Joachim'

def make_app(more_config=None):
    # create app
    app = Flask(__name__)

    # config
    app.config.update({
        'TESTING': True,
        'CODEMIRROR_LANGUAGES': ['python'],
        'CODEMIRROR_THEME': '3024-day',
        'CODEMIRROR_ADDONS': (('dialog', 'dialog'), ('mode', 'overlay')),
        'CODEMIRROR_VERSION': '4.12.0',
        'SECRET_KEY': 'secret!',
    })
    if more_config:
        app.config.update(more_config)

    # codemirror
    codemirror = CodeMirror(app)


    class MyForm(Form):
        code = CodeMirrorField(language='python', id='test',
                            config={'linenumbers': True})


    @app.route('/')
    def index():
        return render_template_string('{{ codemirror.include_codemirror() }}')


    @app.route('/form/')
    def form():
        test_form = MyForm()
        return render_template_string('{{ form.code }}', form=test_form)

    return app


class FlaskCodeMirrorTestBase(unittest.TestCase):
    def setUp(self, more_config=None):
        self.app = make_app(more_config)
        self.app_client = self.app.test_client()


class FlaskCodeMirrorTestHead(FlaskCodeMirrorTestBase):
    def test_head(self):
        response = self.app_client.get('/')
        self.assertIn(
            '<script src="//cdnjs.cloudflare.com/ajax/libs/codemirror/4.12.0/codemirror.js"></script>',
            response.data
        )
        self.assertIn(
            '<link rel="stylesheet" href="//cdnjs.cloudflare.com/ajax/libs/codemirror/4.12.0/codemirror.css">',
            response.data
        )
        self.assertIn(
            '<script src="//cdnjs.cloudflare.com/ajax/libs/codemirror/4.12.0/mode/python/python.js"></script>',
            response.data
        )
        self.assertIn(
            '<link rel="stylesheet" href="//cdnjs.cloudflare.com/ajax/libs/codemirror/4.12.0/theme/3024-day.css">',
            response.data
        )
        self.assertIn(
            '<link rel="stylesheet" href="//cdnjs.cloudflare.com/ajax/libs/codemirror/4.12.0/theme/3024-day.css">',
            response.data
        )
        self.assertIn(
            '<link rel="stylesheet" href="//cdnjs.cloudflare.com/ajax/libs/codemirror/4.12.0/addon/dialog/dialog.css">',
            response.data
        )
        self.assertIn(
            '<script src="//cdnjs.cloudflare.com/ajax/libs/codemirror/4.12.0/addon/dialog/dialog.js"></script>',
            response.data
        )
        self.assertNotIn(
            '<link rel="stylesheet" href="//cdnjs.cloudflare.com/ajax/libs/codemirror/4.12.0/addon/mode/overlay.css">',
            response.data
        )
        self.assertIn(
            '<script src="//cdnjs.cloudflare.com/ajax/libs/codemirror/4.12.0/addon/mode/overlay.js"></script>',
            response.data
        )

class FlaskCodeMirrorTestForm(FlaskCodeMirrorTestBase):
    def test_form(self):
        response = self.app_client.get('/form/')
        self.assertIn(
            '<textarea id="flask-codemirror-test" name="code">',
            response.data
        )
        self.assertIn(
            'var editor_for_test = CodeMirror.fromTextArea(',
            response.data
        )
        self.assertIn(
            'document.getElementById(\'flask-codemirror-test\')',
            response.data
        )
        self.assertIn(
            '"linenumbers": true',
            response.data
        )

class FlaskCodeMirrorTestExc(unittest.TestCase):
    def test_exception(self):
        with self.assertRaises(CodeMirrorConfigException):
            app = make_app({'CODEMIRROR_LANGUAGES': None})


class FlaskCodeMirrorTestLocal(FlaskCodeMirrorTestBase):
    def setUp(self):
        super(FlaskCodeMirrorTestLocal, self).setUp({'CODEMIRROR_SERVE_LOCAL': True})

    def test_head(self):
        response = self.app_client.get('/')
        self.assertIn(
            '<script src="/static/codemirror/4.12.0/codemirror.js"></script>',
            response.data
        )
        self.assertIn(
            '<link rel="stylesheet" href="/static/codemirror/4.12.0/codemirror.css">',
            response.data
        )
        self.assertIn(
            '<script src="/static/codemirror/4.12.0/mode/python/python.js"></script>',
            response.data
        )
        self.assertIn(
            '<link rel="stylesheet" href="/static/codemirror/4.12.0/theme/3024-day.css">',
            response.data
        )
        self.assertIn(
            '<link rel="stylesheet" href="/static/codemirror/4.12.0/theme/3024-day.css">',
            response.data
        )
        self.assertIn(
            '<link rel="stylesheet" href="/static/codemirror/4.12.0/addon/dialog/dialog.css">',
            response.data
        )
        self.assertIn(
            '<script src="/static/codemirror/4.12.0/addon/dialog/dialog.js"></script>',
            response.data
        )
        self.assertIn(
            '<script src="/static/codemirror/4.12.0/addon/mode/overlay.js"></script>',
            response.data
        )


if __name__ == '__main__':
    unittest.main()
