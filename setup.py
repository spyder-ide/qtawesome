# -*- coding: utf-8 -*-

try:
    from setuptools import setup
    from setuptools.command.install import install
except ImportError:
    from distutils.core import setup
    from distutils.core.command.install import install

setup(
    name='QtAwesome',
    version='0.1.0',
    description='FontAwesome icons in PyQt and PySide applications',
    long_description='QtAwesome enables iconic fonts such as Font Awesome and Elusive Icons in your PyQt and PySide application.',
    author='Sylvain Corlay',
    author_email='sylvain.corlay@gmail.com',
    license='MIT License',
    url='https://github.com/spyder-ide/qtawesome',
    keywords=['PyQt', 'PySide', 'Icons'],
    packages=['qtawesome'],
    install_requires=['qtpy'],
    include_package_data=True,
    platforms=['OS-independent'],
)
