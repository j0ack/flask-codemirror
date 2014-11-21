"""
flask-codemirror
----------------

Add a source code field for Flask using Javascript library CodeMirror 
and Fields with WTForms

"""
from setuptools import setup

__version__ = '0.0.3'
__author__ = 'TROUVERIE Joachim'
__contact__ = 'joachim.trouverie@gmail.com'

setup(
    name='flask-codemirror',
    version=__version__,
    url='https://joacodepel.tk/hg/flask-codemirror/',
    license='MIT',
    author=__author__,
    author_email=__contact__,
    description='Use CodeMirror Javascript library with Flask-WTF',
    include_package_data=True,
    long_description=open('README.md').read(),
    packages=['flask_codemirror'],
    zip_safe=False,
    platforms='any',
    install_requires=[
        'Flask',
        'WTForms'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
