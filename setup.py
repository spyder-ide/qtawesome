# -*- coding: utf-8 -*-

try:
    from setuptools import setup
    from setuptools.command.install import install
except ImportError:
    from distutils.core import setup
    from distutils.core.command.install import install

setup(
    name='QtAwesome',
    version='0.1.2',
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
