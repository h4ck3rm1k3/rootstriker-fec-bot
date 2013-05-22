# -*- coding: utf-8  -*-
__version__ = '$Id: rootstikers_family.py 9015 2011-02-28 17:57:55Z lcawte $'

import family

class Family(family.Family):
    def __init__(self):
        family.Family.__init__(self)
        self.name = 'rootstrikers-wikia'

        self.langs = {
            'en': 'rootstrikers.wikia.com',
        }
        # Wikimedia wikis all use "bodyContent" as the id of the <div>
        # element that contains the actual page content; change this for
        # wikis that use something else (e.g., mozilla family)
        self.content_id = "bodyContent"


    # Which version of MediaWiki is used? REQUIRED
    def version(self, code):
        # Replace with the actual version being run on your wiki
        return '1.14'

    def scriptpath(self, code):
        return ''

    def code2encoding(self, code):
        """Return the encoding for a specific language wiki"""
        # Most wikis nowadays use UTF-8, but change this if yours uses
        # a different encoding
        return 'utf-8'
