Welcome to Flask-CodeMirror's documentation
===========================================

Implementation of source code editor for **Flask** and **Flask-WTF**
using **CodeMirror** JavaScript library

Installation
------------

.. code-block:: bash

    $ pip install flask-codemirror

Basic Example
-------------

A simple example of how to use this module::

    from flask_wtf import FlaskForm
    from flask_codemirror.fields import CodeMirrorField
    from wtforms.fields import SubmitField


    class MyForm(FlaskForm):
        source_code = CodeMirrorField(language='python',
                                    config={'lineNumbers' : 'true'})
        submit = SubmitField('Submit')

The ``CodeMirrorField`` works exactly like a ``TextAreaField``::

    @app.route('/', methods = ['GET', 'POST'])
    def index():
        form = MyForm()
        if form.validate_on_submit():
            text = form.source_code.data
        return render_template('index.html', form=form)

The module needs to be initialized in the usual way and can be configured using ``app.config`` keys::

    from flask_codemirror import CodeMirror

    SECRET_KEY = 'secret!'
    # mandatory
    CODEMIRROR_LANGUAGES = ['python', 'html']
    # optional
    CODEMIRROR_THEME = '3024-day'
    CODEMIRROR_ADDONS = (
         ('display','placeholder'),
    )

    app = Flask(__name__)
    app.config.from_object(__name__)
    codemirror = CodeMirror(app)

The config ``CODEMIRROR_LANGUAGES`` needs to be initialized to load JavaScript. It defined all the languages you want to edit with your fields. If the field is not defined a ``CodeMirrorConfigException`` will be raised.

The config ``CODEMIRROR_THEME`` is optional and is used to style your TextArea
using css from `CodeMirror website`_.

The config ``CODEMIRROR_ADDONS`` is optional and can enable many cool options see `Codemirror Addons`_ for available addons.

Finally, the template needs the support JavaScript code added, by calling ``codemirror.include_codemirror()``

.. code-block:: html

    <html>
      <head>
        {{ codemirror.include_codemirror() }}
      </head>
      <body>
        <form method="POST">
          {{ form.csrf_token }}
          {{ form.source_code }}
        </form>
      </body>
    </html>

The JavaScript classes are imported from a CDN, there are no static files that need to be served by the application.

API
---

.. automodule:: flask_codemirror

    .. autoclass:: CodeMirror

        .. automethod:: init_app

    .. autoclass:: CodeMirrorHeaders

        .. automethod:: include_codemirror

.. automodule:: flask_codemirror.fields

    .. autoclass:: CodeMirrorField

.. automodule:: flask_codemirror.widgets

    .. autoclass:: CodeMirrorWidget

        .. automethod:: _generate_content

.. _CodeMirror website: http://codemirror.net/theme/
.. _Codemirror Addons: http://codemirror.net/addon/
