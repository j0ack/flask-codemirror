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
    Flask CodeMirror Widget
    ~~~~~~~~~~~~~~~~~~~~~~~

    Override TextArea widget to append JavaScript
"""

from __future__ import print_function

import json
from flask import current_app
from markupsafe import Markup

try:
    from wtforms.widgets import TextArea
except ImportError as exc:
    print("WTForms is required by Flask-Codemirror")
    raise exc


class CodeMirrorWidget(TextArea):
    """CodeMirror Widget for CodeMirrorField

    Add CodeMirror JavaScript library paramaters to widget

    :param language: source code language
    :param config: CodeMirror field config
    """

    POST_HTML = """
    <script>
        var editor_for_{0} = CodeMirror.fromTextArea(
            document.getElementById('flask-codemirror-{0}'),
            {1}
        );
    </script>
    """

    def __init__(self, language, config=None):
        super(CodeMirrorWidget, self).__init__()
        self.language = language
        self.theme = current_app.config.get("CODEMIRROR_THEME", None)
        self.config = config or {}

    def __call__(self, field, **kwargs):
        field_id = "flask-codemirror-" + field.id
        html = super(CodeMirrorWidget, self).__call__(field, id=field_id, **kwargs)
        content = self._generate_content()
        post_html = self.__class__.POST_HTML.format(field.id, content)
        return html + Markup(post_html)

    def _generate_content(self):
        """Dumps content using JSON to send to CodeMirror"""
        # concat into a dict
        dic = self.config
        dic["mode"] = self.language
        if self.theme:
            dic["theme"] = self.theme
        # dumps with json
        return json.dumps(dic, indent=8, separators=(",", ": "))
