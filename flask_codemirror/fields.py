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
    Flask Codemirror Field
    ~~~~~~~~~~~~~~~~~~~~~~

    Import it using

          `from flask.ext.codemirror.fields import CodeMirrorField`

    It works exactly like a `wtforms.fields.TextAreaField`
"""

from __future__ import print_function

from flask_codemirror.widgets import CodeMirrorWidget
try:
    from wtforms.fields import TextAreaField
except ImportError as exc:
    print('WTForms is required by Flask-Codemirror')
    raise exc


__author__ = 'TROUVERIE Joachim'


class CodeMirrorField(TextAreaField):
    """Code Mirror Field
    A TextAreaField with a custom widget
    :param language: CodeMirror mode
    :param config: CodeMirror config
    """
    def __init__(self, label='', validators=None, language=None,
                 config=None, **kwargs):
        widget = CodeMirrorWidget(language, config)
        super(CodeMirrorField, self).__init__(label=label,
                                              validators=validators,
                                              widget=widget,
                                              **kwargs)
