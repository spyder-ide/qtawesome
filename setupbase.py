# -*- coding: utf-8 -*-
import os
import re
import io
import json
import hashlib
import zipfile
try:
    # Python 2
    from urllib2 import urlopen
except ImportError:
    # Python 3
    from urllib.request import urlopen

import distutils.cmd
import distutils.log

HERE = os.path.abspath(os.path.dirname(__file__))


class UpdateFA5Command(distutils.cmd.Command):
    """A custom command to make updating FontAwesome 5.x easy!"""
    description = 'Try to update the FontAwesome 5.x data in the project.'
    user_options = [
        ('fa-version=', None, 'FA version.'),
        ('zip-path=', None, 'Read from local zip file path.'),
    ]

    # Update these below if the FontAwesome changes their structure:
    FA_STYLES = ('regular', 'solid', 'brands')
    CHARMAP_PATH_TEMPLATE = os.path.join(HERE, 'qtawesome', 'fonts', 'fontawesome5-{style}-webfont-charmap.json')
    TTF_PATH_TEMPLATE = os.path.join(HERE, 'qtawesome', 'fonts', 'fontawesome5-{style}-webfont.ttf')
    ICONIC_FONT_PY_PATH = os.path.join(HERE, 'qtawesome', 'iconic_font.py')
    URL_TEMPLATE = 'https://github.com/FortAwesome/Font-Awesome/' \
        'releases/download/{version}/fontawesome-free-{version}-web.zip'

    def initialize_options(self):
        """Set default values for the command options."""
        self.fa_version = ''
        self.zip_path = ''

    def finalize_options(self):
        """Validate the command options."""
        assert bool(self.fa_version), 'FA version is mandatory for this command.'
        if self.zip_path:
            assert os.path.exists(self.zip_path), (
                'Local zipfile does not exist: %s' % self.zip_path)

    def __print(self, msg):
        """Shortcut for printing with the distutils logger."""
        self.announce(msg, level=distutils.log.INFO)

    def __get_charmap_path(self, style):
        """Get the project FA charmap path for a given style."""
        return self.CHARMAP_PATH_TEMPLATE.format(style=style)

    def __get_ttf_path(self, style):
        """Get the project FA font path for a given style."""
        return self.TTF_PATH_TEMPLATE.format(style=style)

    @property
    def __release_url(self):
        """Get the release URL."""
        return self.URL_TEMPLATE.format(version=self.fa_version)

    @property
    def __zip_file(self):
        """Get a file object of the FA zip file."""
        if self.zip_path:
            # If using a local file, just open it:
            self.__print('Opening local zipfile: %s' % self.zip_path)
            return open(self.zip_path, 'rb')

        # Otherwise, download it and make a file object in-memory:
        url = self.__release_url
        self.__print('Downloading from URL: %s' % url)
        response = urlopen(url)
        return io.BytesIO(response.read())

    @property
    def __zipped_files_data(self):
        """Get a dict of all files of interest from the FA release zipfile."""
        files = {}
        with zipfile.ZipFile(self.__zip_file) as thezip:
            for zipinfo in thezip.infolist():
                if zipinfo.filename.endswith('metadata/icons.json'):
                    with thezip.open(zipinfo) as compressed_file:
                        files['icons.json'] = compressed_file.read()
                elif zipinfo.filename.endswith('.ttf'):
                    # For the record, the paths usually look like this:
                    # webfonts/fa-brands-400.ttf
                    # webfonts/fa-regular-400.ttf
                    # webfonts/fa-solid-900.ttf
                    name = os.path.basename(zipinfo.filename)
                    tokens = name.split('-')
                    style = tokens[1]
                    if style in self.FA_STYLES:
                        with thezip.open(zipinfo) as compressed_file:
                            files[style] = compressed_file.read()

        # Safety checks:
        assert all(style in files for style in self.FA_STYLES), \
            'Not all FA styles found! Update code is broken.'
        assert 'icons.json' in files, 'icons.json not found! Update code is broken.'

        return files

    def run(self):
        """Run command."""
        files = self.__zipped_files_data
        hashes = {}
        icons = {}

        # Read icons.json (from the webfont zip download)
        data = json.loads(files['icons.json'])

        # Group icons by style, since not all icons exist for all styles:
        for icon, info in data.iteritems():
            for style in info['styles']:
                icons.setdefault(str(style), {})
                icons[str(style)][icon] = str(info['unicode'])

        # For every FA "style":
        for style, details in icons.iteritems():
            # Dump a .json charmap file:
            charmapPath = self.__get_charmap_path(style)
            self.__print('Dumping updated "%s" charmap: %s' % (style, charmapPath))
            with open(charmapPath, 'w+') as f:
                json.dump(details, f, indent=4, sort_keys=True)

            # Dump a .ttf font file:
            fontPath = self.__get_ttf_path(style)
            data = files[style]
            hashes[style] = hashlib.md5(data).hexdigest()
            self.__print('Dumping updated "%s" font: %s' % (style, fontPath))
            with open(fontPath, 'w+') as f:
                f.write(data)

        # Now it's time to patch "iconic_font.py":
        iconic_path = self.ICONIC_FONT_PY_PATH
        self.__print('Patching new MD5 hashes in: %s' % iconic_path)
        with open(iconic_path, 'r') as iconic_file:
            contents = iconic_file.read()
        # We read it in full, then use regex substitution:
        for style, md5 in hashes.iteritems():
            self.__print('New "%s" hash is: %s' % (style, md5))
            regex = r"('fontawesome5-%s-webfont.ttf':\s+)'(\w+)'" % style
            subst = r"\g<1>'" + md5 + "'"
            contents = re.sub(regex, subst, contents, 1)
        # and finally overwrite with the modified file:
        self.__print('Dumping updated file: %s' % iconic_path)
        with open(iconic_path, 'w') as iconic_file:
            iconic_file.write(contents)

        self.__print(
            '\nFinished!\n'
            'Please check the git diff to make sure everything went okay.\n'
            'You should also edit README.md and '
            'qtawesome/docs/source/usage.rst to reflect the changes.')
