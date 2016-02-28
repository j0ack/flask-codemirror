Flask-CodeMirror
================

Implementation of source code editor for Flask and Flask-WTF using CodeMirror Javascript library

Installation
------------

     $ pip install flask-codemirror

Example
-------
A simple example of how to use this module

    .. code:: python
	      
      from flask.ext.wtf import form
      from flask.ext.codemirror.fields import CodeMirrorField
      from wtforms.fields import SubmitField
      
      class MyForm(Form):
          source_code = CodeMirrorField(language='python', config={'lineNumbers' : 'true'})
          submit = SubmitField('Submit')

The `CodeMirrorField` works exactly like a `TextAreaField`

    .. code:: python
	      
      @app.route('/', methods = ['GET', 'POST'])
      def index():
          form = MyForm()
          if form.validate_on_submit():
              text = form.source_code.data
          return render_template('index.html', form = form)

The module needs to be initialized in the usual way and can be configured using app.config keys

    .. code:: python
	      
      from flask.ext.codemirror import CodeMirror
      # mandatory
      CODEMIRROR_LANGUAGES = ['python', 'html']
      # optional
      CODEMIRROR_THEME = '3024-day'
      CODEMIRROR_ADDONS = (
                  ('ADDON_DIR','ADDON_NAME'),
      )
      app = Flask(__name__)
      app.config.from_object(__name__)
      codemirror = CodeMirror(app)

The config `CODEMIRROR_LANGUAGES` needs to be initialized to load JavaScript. It defined all the languages you want to edit with your fields.
The config `CODEMIRROR_THEME` is optional and is used to style your TextArea using css from `CodeMirror website <http://codemirror.net/theme/>`_.
The config `CODEMIRROR_ADDONS` is optional and can enable many cool options see `Codemirror Addons <http://codemirror.net/addon/>`_ for available addons.

Finally, the template needs the support Javascript code added, by calling `codemirror.include_codemirror()` :

    .. code:: django

       <html>
         <head>
           {{ codemirror.include_codemirror() }}
         </head>
         <body>
	   <form method="POST">
              {{ form.source_code }}
	      <input type="submit" value="OK">
           </form>
         </body>
       </html>


The Javascript classes are imported from a CDN, there are no static files that need to be served by the application.

