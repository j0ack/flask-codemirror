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
from flask_wtf import FlaskForm
from flask_codemirror import CodeMirror, CodeMirrorConfigException
from flask_codemirror.fields import CodeMirrorField


__author__ = 'TROUVERIE Joachim'

# create app
app = Flask(__name__)

# config
CODEMIRROR_LANGUAGES = ['python']
CODEMIRROR_THEME = '3024-day'
CODEMIRROR_ADDONS = (('dialog', 'dialog'), ('mode', 'overlay'))
CODEMIRROR_VERSION = '5.61.0'
SECRET_KEY = 'secret!'
app.config.from_object(__name__)

# codemirror
codemirror = CodeMirror(app)


class MyForm(FlaskForm):
    code = CodeMirrorField(language='python', id='test',
                           config={'linenumbers': True})


@app.route('/')
def index():
    return render_template_string('{{ codemirror.include_codemirror() }}')


@app.route('/form/')
def form():
    test_form = MyForm()
    return render_template_string('{{ form.code }}', form=test_form)


class FlaskCodeMirrorTest(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()

    def test_head(self):
        response = self.app.get('/')
        self.assertIn(
            b'<script src="//cdnjs.cloudflare.com/ajax/libs/codemirror/5.61.0/codemirror.js"></script>',
            response.data
        )
        self.assertIn(
            b'<link rel="stylesheet" href="//cdnjs.cloudflare.com/ajax/libs/codemirror/5.61.0/codemirror.css">',
            response.data
        )
        self.assertIn(
            b'<script src="//cdnjs.cloudflare.com/ajax/libs/codemirror/5.61.0/mode/python/python.js"></script>',
            response.data
        )
        self.assertIn(
            b'<link rel="stylesheet" href="//cdnjs.cloudflare.com/ajax/libs/codemirror/5.61.0/theme/3024-day.css">',
            response.data
        )
        self.assertIn(
            b'<link rel="stylesheet" href="//cdnjs.cloudflare.com/ajax/libs/codemirror/5.61.0/theme/3024-day.css">',
            response.data
        )
        self.assertIn(
            b'<link rel="stylesheet" href="//cdnjs.cloudflare.com/ajax/libs/codemirror/5.61.0/addon/dialog/dialog.css">',
            response.data
        )
        self.assertIn(
            b'<script src="//cdnjs.cloudflare.com/ajax/libs/codemirror/5.61.0/addon/dialog/dialog.js"></script>',
            response.data
        )
        self.assertNotIn(
            b'<link rel="stylesheet" href="//cdnjs.cloudflare.com/ajax/libs/codemirror/5.61.0/addon/mode/overlay.css">',
            response.data
        )
        self.assertIn(
            b'<script src="//cdnjs.cloudflare.com/ajax/libs/codemirror/5.61.0/addon/mode/overlay.js"></script>',
            response.data
        )

    def test_form(self):
        response = self.app.get('/form/')
        self.assertIn(
            b'<textarea id="flask-codemirror-test" name="code">',
            response.data
        )
        self.assertIn(
            b'var editor_for_test = CodeMirror.fromTextArea(',
            response.data
        )
        self.assertIn(
            b'document.getElementById(\'flask-codemirror-test\')',
            response.data
        )
        self.assertIn(
            b'"linenumbers": true',
            response.data
        )

    def test_exception(self):
        app.config['CODEMIRROR_LANGUAGES'] = None
        with self.assertRaises(CodeMirrorConfigException):
            CodeMirror(app)

if __name__ == '__main__':
    unittest.main()
