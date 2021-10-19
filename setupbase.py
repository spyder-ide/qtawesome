# -*- coding: utf-8 -*-
import os
import re
import io
import sys
import csv
import json
import shutil
import hashlib
import zipfile
import tempfile

try:
    from fontTools import ttLib
except ImportError:
    ttLib = None

from urllib.request import urlopen

import distutils.cmd
import distutils.log

HERE = os.path.abspath(os.path.dirname(__file__))
ICONIC_FONT_PY_PATH = os.path.join(HERE, 'qtawesome', 'iconic_font.py')


def rename_font(font_path, font_name):
    """
    Font renaming code originally from:
    https://github.com/chrissimpkins/fontname.py/blob/master/fontname.py
    """
    tt = ttLib.TTFont(font_path)
    namerecord_list = tt["name"].names
    variant = ""

    # determine font variant for this file path from name record nameID 2
    for record in namerecord_list:
        if record.nameID == 2:
            variant = str(record)
            break

    # test that a variant name was found in the OpenType tables of the font
    if len(variant) == 0:
        raise ValueError(
            "Unable to detect the font variant from the OpenType name table in: %s" % font_path)

    # Here are some sample name records to give you an idea of the name tables:
    # ID 0: 'Copyright (c) Font Awesome'
    # ID 1: 'Font Awesome 5 Free Regular'
    # ID 2: 'Regular'
    # ID 3: 'Font Awesome 5 Free Regular-5.14.0'
    # ID 4: 'Font Awesome 5 Free Regular'
    # ID 5: '331.264 (Font Awesome version: 5.14.0)'
    # ID 6: 'FontAwesome5Free-Regular'
    # ID 10: "The web's most popular icon set and toolkit."
    # ID 11: 'https://fontawesome.com'
    # ID 16: 'Font Awesome 5 Free'
    # ID 17: 'Regular'
    # ID 18: 'Font Awesome 5 Free Regular'
    # ID 21: 'Font Awesome 5 Free'
    # ID 22: 'Regular'

    # modify the opentype table data in memory with updated values
    for record in namerecord_list:
        if record.nameID in (1, 4, 16, 21):
            print(f"Renaming font name record at ID {record.nameID}: {record.string} --> {font_name}")
            record.string = font_name

    # write changes to the font file
    try:
        tt.save(font_path)
    except:
        raise RuntimeError(
            f"ERROR: unable to write new name to OpenType tables for: {font_path}")


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
        for icon, info in data.items():
            for style in info['styles']:
                icons.setdefault(str(style), {})
                icons[str(style)][icon] = str(info['unicode'])

        # For every FA "style":
        for style, details in icons.items():
            # Dump a .json charmap file:
            charmapPath = self.__get_charmap_path(style)
            self.__print('Dumping updated "%s" charmap: %s' % (style, charmapPath))
            with open(charmapPath, 'w+') as f:
                json.dump(details, f, indent=4, sort_keys=True)

            # Dump a .ttf font file:
            font_path = self.__get_ttf_path(style)
            data = files[style]
            self.__print('Dumping updated "%s" font: %s' % (style, font_path))
            with open(font_path, 'wb+') as f:
                f.write(data)

            # Fix to prevent repeated font names:
            if style in ('regular', 'solid'):
                new_name = str("Font Awesome 5 Free %s") % style.title()
                self.__print('Renaming font to "%s" in: %s' % (new_name, font_path))
                if ttLib is not None:
                    rename_font(font_path, new_name)
                else:
                    sys.exit(
                        "This special command requires the module 'fonttools': "
                        "https://github.com/fonttools/fonttools/")

                # Reread the data since we just edited the font file:
                with open(font_path, 'rb') as f:
                    data = f.read()
                    files[style] = data

            # Store hashes for later:
            hashes[style] = hashlib.md5(data).hexdigest()

        # Now it's time to patch "iconic_font.py":
        iconic_path = ICONIC_FONT_PY_PATH
        self.__print('Patching new MD5 hashes in: %s' % iconic_path)
        with open(iconic_path, 'r') as iconic_file:
            contents = iconic_file.read()
        # We read it in full, then use regex substitution:
        for style, md5 in hashes.items():
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


class UpdateCodiconCommand(distutils.cmd.Command):
    """A custom command to make updating Microsoft's Codicons easy!"""
    description = 'Try to update the Codicon font data in the project.'
    user_options = []

    CHARMAP_PATH = os.path.join(HERE, 'qtawesome', 'fonts', 'codicon-charmap.json')
    TTF_PATH = os.path.join(HERE, 'qtawesome', 'fonts', 'codicon.ttf')
    DOWNLOAD_URL_TTF = 'https://raw.githubusercontent.com/microsoft/vscode-codicons/master/dist/codicon.ttf'
    DOWNLOAD_URL_CSV = 'https://raw.githubusercontent.com/microsoft/vscode-codicons/master/dist/codicon.csv'
    # At the time of writing this comment, vscode-codicons repo does not use git tags, but you can get the version from package.json:
    DOWNLOAD_URL_JSON = 'https://raw.githubusercontent.com/microsoft/vscode-codicons/master/package.json'

    def initialize_options(self):
        """Required by distutils."""

    def finalize_options(self):
        """Required by distutils."""

    def __print(self, msg):
        """Shortcut for printing with the distutils logger."""
        self.announce(msg, level=distutils.log.INFO)

    def run(self):
        """Run command."""

        # Download .csv to a temporary path:
        package_json = urlopen(self.DOWNLOAD_URL_JSON)
        package_info = json.load(package_json)
        package_version = package_info['version']
        self.__print('Will download codicons version: %s' % package_version)

        # Download .csv to a temporary path:
        with tempfile.NamedTemporaryFile(mode='wb+', suffix='.csv', prefix='codicon', delete=False) as tempCSV:
            self.__print('Downloading: %s' % self.DOWNLOAD_URL_CSV)
            response = urlopen(self.DOWNLOAD_URL_CSV)
            shutil.copyfileobj(response, tempCSV)

        # Interpret the codicon.csv file:
        charmap = {}
        with open(tempCSV.name, 'r', encoding='utf-8') as tempCSV:
            reader = csv.DictReader(tempCSV)
            for row in reader:
                code = "0x" + row['unicode'].lower()
                charmap[row['short_name']] = code
        self.__print('Identified %s icons in the CSV.' % len(charmap))

        # Remove temp file:
        os.remove(tempCSV.name)

        # Dump a .json charmap file the way we like it:
        self.__print('Dumping updated charmap: %s' % self.CHARMAP_PATH)
        with open(self.CHARMAP_PATH, 'w+') as f:
            json.dump(charmap, f, indent=4, sort_keys=True)

        # Dump a .ttf font file:
        with open(self.TTF_PATH, 'wb+') as ttfFile:
            self.__print('Downloading %s --> %s' % (self.DOWNLOAD_URL_TTF, self.TTF_PATH))
            response = urlopen(self.DOWNLOAD_URL_TTF)
            data = response.read()
            ttfFile.write(data)
            md5 = hashlib.md5(data).hexdigest()
            self.__print('New hash is: %s' % md5)

        # Now it's time to patch "iconic_font.py":
        self.__print('Patching new MD5 hashes in: %s' % ICONIC_FONT_PY_PATH)
        with open(ICONIC_FONT_PY_PATH, 'r') as iconic_file:
            contents = iconic_file.read()
        regex = r"('codicon.ttf':\s+)'(\w+)'"
        subst = r"\g<1>'" + md5 + "'"
        contents = re.sub(regex, subst, contents, 1)
        self.__print('Dumping updated file: %s' % ICONIC_FONT_PY_PATH)
        with open(ICONIC_FONT_PY_PATH, 'w') as iconic_file:
            iconic_file.write(contents)

        self.__print(
            '\nFinished!\n'
            'Please check the git diff to make sure everything went okay.\n'
            'You should also edit README.md and '
            'qtawesome/docs/source/usage.rst to reflect the changes.')
