# -*- coding: utf-8 -*-
import os
import io
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

with io.open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    LONG_DESCRIPTION = f.read()

setup(
    name='QtAwesome',
    version=version_ns['__version__'],
    description='FontAwesome icons in PyQt and PySide applications',
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
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
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: User Interfaces',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',]
)
