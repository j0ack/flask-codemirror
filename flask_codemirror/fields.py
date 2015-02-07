#! /usr/bin/env python
#-*- coding : utf-8 -*-

"""
    Flask Codemirror Field
    ~~~~~~~~~~~~~~~~~~~~~~

    Import it using

          `from flask.ext.codemirror.fields import CodeMirrorField`

    It works exactly like a `wtforms.fields.TextAreaField`
"""

from .widgets import CodeMirrorWidget
try :
    from wtforms.fields import TextAreaField
except ImportError as exc :
    print('WTForms is required by Flask-Codemirror')
    raise exc


__author__ = 'TROUVERIE Joachim'


class CodeMirrorField(TextAreaField):
    """Code Mirror Field

    A TextAreaField with a custom widget 
        
    :param language: CodeMirror mode
    :param config: CodeMirror config
    """
    def __init__(self, label='', validators = None, language = None, 
                 config = None, **kwargs) :
        widget = CodeMirrorWidget(language, config)
        super(CodeMirrorField, self).__init__(label=label, 
                                                validators = validators,
                                                widget = widget, **kwargs)
