#! /usr/bin/env python
#-*- coding : utf-8 -*-
# vim:set shiftwidth=4 tabstop=4 expandtab textwidth=79:

"""
   Field for Flask Codemirror
"""

from .widgets import CodeMirrorWidget
try :
    from wtforms.fields import TextAreaField
except ImportError, exc :
    print 'WTForms is required by Flask-Codemirror'
    raise exc

class CodeMirrorField(TextAreaField):
    """
        Code Mirror Field

        Override TextArea Widget
        
        :param : language : str - CodeMirror mode
        :param : config : dict - CodeMirror config
    """
    def __init__(self, label='', validators=None, language=None, 
                 config=None, **kwargs) :        
        super(CodeMirrorField, self).__init__(label=label, 
                                              validators=validators,
                                              widget = CodeMirrorWidget(language, config),
                                              **kwargs)
