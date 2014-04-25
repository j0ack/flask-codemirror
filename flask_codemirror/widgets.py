#! /usr/bin/env python
#-*- coding : utf-8 -*-
# vim:set shiftwidth=4 tabstop=4 expandtab textwidth=79:

"""
    CodeMirror Widget for CodeMirrorField
"""

from flask import current_app
import json
try :
    from wtforms.widgets import HTMLString, TextArea  
except ImportError, exc :
    print 'WTForms is required by Flask-Codemirror'
    raise exc

class CodeMirrorWidget(TextArea):
    """
        CodeMirror Widget for CodeMirrorField

        Add language and theme support to widget

        :param : in_language : str - program language for textarea
        :param : in_config   : dict - CodeMirror field config
    """

    post_html = '''
    <script>
        var editor_for_{0} = CodeMirror.fromTextArea(
            document.getElementById('flask-codemirror-{0}'), 
            {1}   
        );
    </script>
    '''

    def __init__(self, in_language, in_config = None) :
        super(CodeMirrorWidget, self).__init__()        
        self.language = in_language
        self.theme    = current_app.config.get('CODEMIRROR_THEME', None)
        self.config   = in_config or {}

    def __call__(self, field, **kwargs):
        html = super(CodeMirrorWidget, self).__call__(field, 
                    id='flask-codemirror-' + field.name, **kwargs)
        content = self._generate_content()
        post_html = self.__class__.post_html.format(field.name, content)
        return HTMLString(html + post_html)

    def _generate_content(self) :
        """
            Dumps content using JSON to send to CodeMirror
        """
        # concat into a dict
        dic = self.config
        dic['mode'] = self.language
        if self.theme :
            dic['theme'] = self.theme
        # dumps with json
        return json.dumps(dic, indent=8, separators=(',', ': '))
