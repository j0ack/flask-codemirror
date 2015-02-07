"""
flask-codemirror
----------------

Add a source code field for Flask using Javascript library CodeMirror 
and Fields with WTForms

"""
from setuptools import setup

__version__ = '0.0.4'
__author__ = 'TROUVERIE Joachim'
__contact__ = 'joachim.trouverie@joacodepel.tk'

setup(
    name='flask-codemirror',
    version=__version__,
    url='https://github.com/j0ack/flask-codemirror',
    license='GPL',
    author=__author__,
    author_email=__contact__,
    description='Use CodeMirror Javascript library with Flask-WTF',
    include_package_data=True,
    long_description=open('README.rst').read(),
    packages=['flask_codemirror'],
    zip_safe=False,
    platforms='any',
    install_requires=[
        'Flask',
        'WTForms',
        'requests'
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Framework :: Flask',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities'
    ]
)
