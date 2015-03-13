"""
Ugly script used to summarize all pelican-themes.
https://github.com/getpelican/pelican-themes.

Place this script one level below THEMES_DIR.
It will generate summary.html containing the themes.  
"""
import os
from collections import OrderedDict as od

THEMES_DIR = 'pelican-themes'

# first, discover all themes that have screenshots
# each screenshot's filename is stored
contents = os.listdir(THEMES_DIR)
accumulated_screenshots = od()
for entry in contents:
    theme_directory = os.path.join(THEMES_DIR, entry)
    if os.path.isdir(theme_directory) and entry != '.git':
        theme_contents = os.listdir(theme_directory)
        accumulated_screenshots[entry] = []
        for theme_file in theme_contents:
            if theme_file[-3:] in ('jpg', 'png', 'gif'):
                accumulated_screenshots[entry].append(theme_file)

# second, create an HTML file
# the IMG elements point to the accumulated screenshots
to_write = ['<html><body>\n']
for theme, screenshots in accumulated_screenshots.iteritems():
    path = os.path.join(THEMES_DIR, theme)
    for i, screenshot in enumerate(screenshots):
        if i == 0:
            # print the theme's name only once
            to_write.append('<h1>%s</h1><br />\n' % theme)
        screenshot_path = os.path.join(path, screenshot)
        to_write.append('<center>\n')
        to_write.append(
            '<img src="%s" height=500>\n' % screenshot_path
        )
        to_write.append('</center><br />\n')
    to_write.append('<br />\n')
to_write.append('</body></html>\n')

with open('summary.html', 'w') as f:
    f.writelines(to_write)
