# -*- coding: utf-8 -*-
import os
try:
    from setuptools import setup
    from setuptools.command.install import install
except ImportError:
    from distutils.core import setup
    from distutils.core.command.install import install

here = os.path.abspath(os.path.dirname(__file__))

version_ns = {}
with open(os.path.join(here, 'qtawesome', '_version.py')) as f:
    exec(f.read(), {}, version_ns)

LONG_DESCRIPTION = """
.. image:: https://img.shields.io/pypi/v/QtAwesome.svg
   :target: https://pypi.python.org/pypi/QtAwesome/
   :alt: Latest PyPI version

.. image:: https://img.shields.io/pypi/dm/QtAwesome.svg
   :target: https://pypi.python.org/pypi/QtAwesome/
   :alt: Number of PyPI downloads

QtAwesome - Iconic Fonts in PyQt and PySide applications
========================================================

QtAwesome enables iconic fonts such as Font Awesome and Elusive Icons in PyQt and PySide applications.

It is a port to Python - PyQt / PySide of the QtAwesome C++ library by Rick Blommers.

.. code-block:: python

    # Get icons by name.
    fa_icon = qta.icon('fa.flag')
    fa_button = QtGui.QPushButton(fa_icon, 'Font Awesome!')

    asl_icon = qta.icon('ei.asl')
    elusive_button = QtGui.QPushButton(asl_icon, 'Elusive Icons!')
"""

setup(
    name='QtAwesome',
    version=version_ns['__version__'],
    description='FontAwesome icons in PyQt and PySide applications',
    long_description=LONG_DESCRIPTION,
    author='Sylvain Corlay',
    author_email='sylvain.corlay@gmail.com',
    license='MIT',
    url='https://github.com/spyder-ide/qtawesome',
    keywords=['PyQt', 'PySide', 'Icons', 'Font Awesome', 'Fonts'],
    packages=['qtawesome'],
    install_requires=['qtpy', 'six'],
    include_package_data=True,
    platforms=['OS-independent'],
    classifiers=[
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Topic :: Software Development :: User Interfaces',

        # License
        'License :: OSI Approved :: MIT License',

        # Supported Python versions
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',]
)
