#! /usr/bin/env python

from flask import Flask, render_template
from flask.ext.codemirror import CodeMirror
from flask.ext.codemirror.fields import CodeMirrorField
from flask.ext.wtf import Form
from wtforms.fields import SubmitField

CODEMIRROR_LANGUAGES = ['python']
CODEMIRROR_THEME = '3024-day'
DEBUG = True
SECRET_KEY = 'codemirror'

app = Flask(__name__)
app.config.from_object(__name__)
codemirror = CodeMirror(app)

class MyForm(Form):
    source = CodeMirrorField('Test', language='python', config={'lineNumbers' : 'true'})
    submit = SubmitField('Submit')

@app.route('/', methods = ['GET', 'POST'])
def index():
    form = MyForm()
    if form.validate_on_submit():
       return form.source.data
    return render_template('index.html', form = form)

