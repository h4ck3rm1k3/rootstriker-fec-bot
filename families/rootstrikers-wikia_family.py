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
        self.namespaces[4] = {            'en': 'Rootstrikers Wiki',        }
        self.namespaces[5] = {            'en': 'Rootstrikers Wiki talk',        }
        self.namespaces[110] = {            'en': 'Forum',        }
        self.namespaces[111] = {            'en': 'Forum talk',        }
        self.namespaces[500] = {            'en': 'User blog',        }
        self.namespaces[501] = {            'en': 'User blog comment',        }
        self.namespaces[502] = {            'en': 'Blog',        }
        self.namespaces[503] = {            'en': 'Blog talk',        }
        self.namespaces[1200] = {            'en': 'Message Wall',        }
        self.namespaces[1201] = {            'en': 'Thread',        }
        self.namespaces[1202] = {            'en': 'Message Wall Greeting',        }

        # Wikimedia wikis all use "bodyContent" as the id of the <div>
        # element that contains the actual page content; change this for
        # wikis that use something else (e.g., mozilla family)
        self.content_id = "bodyContent"


    # Which version of MediaWiki is used? REQUIRED
    def version(self, code):
        # Replace with the actual version being run on your wiki
        return '1.19.7'

    def scriptpath(self, code):
        return ''

    def code2encoding(self, code):
        """Return the encoding for a specific language wiki"""
        # Most wikis nowadays use UTF-8, but change this if yours uses
        # a different encoding
        return 'utf-8'
