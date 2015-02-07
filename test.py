#! /usr/bin/env python

"""
    Flask Codemirror Test
    ~~~~~~~~~~~~~~~~~~~~~

    Unit tests for Flask-CodeMirror
"""

__author__ = 'TROUVERIE Joachim'

import unittest

from flask import Flask, render_template_string
from flask.ext.wtf import Form
from flask_codemirror import CodeMirror, CodeMirrorConfigException
from flask_codemirror.fields import CodeMirrorField

# create app
app = Flask(__name__)

# config
CODEMIRROR_LANGUAGES = ['python']
CODEMIRROR_THEME = '3024-day'
CODEMIRROR_ADDONS = (('dialog','dialog'),('mode', 'overlay'))
CODEMIRROR_VERSION = '4.12.0'
SECRET_KEY = 'secret!'
app.config.from_object(__name__)

# codemirror
codemirror = CodeMirror(app)


class MyForm(Form) :
    code = CodeMirrorField(language = 'python', id = 'test',
                            config = {'linenumbers' : True})

    
@app.route('/')
def index() :
    return render_template_string('{{ codemirror.include_codemirror() }}')


@app.route('/form/')
def form() :
    test_form = MyForm()
    return render_template_string('{{ form.code }}', form = test_form)


class FlaskCodeMirrorTest(unittest.TestCase) :
    def setUp(self) :
        app.config['TESTING'] = True
        self.app = app.test_client()


    def test_head(self) :
        response = self.app.get('/')
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
        

    def test_form(self) :
        response = self.app.get('/form/')
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
        
        
    def test_exception(self) :
        app.config['CODEMIRROR_LANGUAGES'] = None
        with self.assertRaises(CodeMirrorConfigException) :
            codemirror = CodeMirror(app)
        
        
if __name__ == '__main__' :
    unittest.main()
