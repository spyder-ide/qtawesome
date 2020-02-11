# -*- coding: utf-8 -*-
import os
import io

try:
    from setuptools import setup
    from setuptools.command.install import install
except ImportError:
    from distutils.core import setup
    from distutils.core.command.install import install

# Code to add custom build commands comes from here:
import setupbase

HERE = os.path.abspath(os.path.dirname(__file__))

VERSION_NS = {}
with open(os.path.join(HERE, 'qtawesome', '_version.py')) as f:
    exec(f.read(), {}, VERSION_NS)

with io.open(os.path.join(HERE, 'README.md'), encoding='utf-8') as f:
    LONG_DESCRIPTION = f.read()


setup(
    name='QtAwesome',
    version=VERSION_NS['__version__'],
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
        'Programming Language :: Python :: 3', ],
    cmdclass={
        'update_fa5': setupbase.UpdateFA5Command,
    },
    entry_points={
        'console_scripts': ['qta-browser=qtawesome.icon_browser:run'],
    }
)
