#!/usr/bin/python
# -*- coding: utf-8  -*-
"""
This is not a complete bot; rather, it is a template from which simple
bots can be made. You can rename it to mybot.py, then edit it in
whatever way you want.

The following parameters are supported:

&params;

-dry              If given, doesn't do any real changes, but only shows
                  what would have been changed.

All other parameters will be regarded as part of the title of a single page,
and the bot will only work on that single page.
"""
# (C) James Michael DuPont, 2013
# (C) Pywikipedia bot team, 2006-2010
#
# Distributed under the terms of the MIT license.
#
__version__ = '$Id: basic.py 8807 2010-12-27 21:34:11Z purodha $'
#
import unicodedata
import wikipedia as pywikibot
import pagegenerators
import types
import sys
#sys.path.append("../maplight-convert/") 
sys.path.append("../") 

import legislators_current as leg
legs= leg.load()

maplight={}
for x in sorted(legs['wp'].keys()):
    if ('maplight' in legs['wp'][x]['id'] ):
        maplightid= str(legs['wp'][x]['id']['maplight'])
        maplight[maplightid]=legs['wp'][x]
    else:
        print "no maplight in %s" % x


# This is required for the text that is shown when you run this script
# with the parameter -help.
docuReplacements = {
    '&params;': pagegenerators.parameterHelp
}
import re

class BasicBot:
    # Edit summary message that should be used.
    # NOTE: Put a good description here, and add translations, if possible!
    msg = {
        'en': u'Rootstriker bot: Adding in cong links',
    }

    def __init__(self, generator, dry):
        """
        Constructor. Parameters:
            @param generator: The page generator that determines on which pages
                              to work.
            @type generator: generator.
            @param dry: If True, doesn't do any real changes, but only shows
                        what would have been changed.
            @type dry: boolean.
        """
        self.generator = generator
        self.dry = dry
        # Set the edit summary message
        self.summary = pywikibot.translate(pywikibot.getSite(), self.msg)

    def run(self):
        for page in self.generator:
            self.treat(page)

    def treat(self, page):
        """
        Loads the given page, does some changes, and saves it.
        """
        text = self.load(page)
        if not text:
            return

        ################################################################
        # NOTE: Here you can modify the text in whatever way you want. #
        ################################################################

        # If you find out that you do not want to edit this page, just return.
        # Example: This puts the text 'Test' at the beginning of the page.
#        text = 'Test ' + text

        # get the maplight id.

#{{maplight candidate||all_count=567|all_rank=211|chamber_count=508|chamber_rank=177|contrib_end=May 19, 2013|contrib_start=Jan 1, 2013|contrib_total=135310|district_holding=8|district_running=8|first_name=Larry|full_name=Larry D Bucshon|gender=M|ico=I|last_name=Bucshon|office_holding=House|office_running=House|party=Republican|person_id=5705|state=IN|status=Not Yet A Statutory Candidate|status_date=|url_photo=http://images.maplight.org/persons/5705.jpg}}
#        print text 

        regex = re.compile(r'.*CongLinks.*', re.MULTILINE)
        matches = [m.groups(0) for m in regex.finditer(text)]
        if matches:
            pywikibot.output(u'Page %s already contains CongLinks.' % page.title(asLink=True))
            return 

        regex = re.compile(r'.*\|person_id\=(\d+)\|.*', re.MULTILINE)
        matches = [m.groups(0) for m in regex.finditer(text)]
    
        if (matches ):
            pywikibot.output(u'Page %s being edited.' % page.title(asLink=True))
            maplightid=str(matches[0][0])
#            print maplightid
            if maplightid in maplight:
                data=maplight[maplightid]

                ids = "\n{{CongLinks"
                for k in  data['id'].keys() :
                    if (k == 'fec') :
                        fecs = "{{fecids"
                        for fec in data['id'][k] :
                            fecs = fecs +  "|" + str(fec) 
                        fecs = fecs + "}}"
                        ids = ids +  "|" + str(k) +  "=" + str(fecs)
                    else:
                        val =data['id'][k]
                        if type(val) == types.IntType :
                            val = str(val)
                            
#                        print type(data['id'][k])
 #                       print data['id'][k]
  #                      val =unicode(data['id'][k],'utf-8')
                        ids = ids +  "|" + str(k) +  "=" + val

#                            )
 #                       except :
 #                           print "canot add key", k, data['id'][k]
                ids = ids +  "}}"
                text =  text + ids

            else:
                print maplightid
                print maplight.keys()
        else:
            print "no person id found"
        try:
            if not self.save(text, page, self.summary):
                pywikibot.output(u'Page %s not saved.' % page.title(asLink=True))
        except :
            pass

    def load(self, page):
        """
        Loads the given page, does some changes, and saves it.
        """
        try:
            # Load the page
            text = page.get()
        except pywikibot.NoPage:
            pywikibot.output(u"Page %s does not exist; skipping."
                             % page.title(asLink=True))
        except pywikibot.IsRedirectPage:
            pywikibot.output(u"Page %s is a redirect; skipping."
                             % page.title(asLink=True))
        else:
            return text
        return None

    def save(self, text, page, comment, minorEdit=True, botflag=True):
        # only save if something was changed
        if text != page.get():
            # Show the title of the page we're working on.
            # Highlight the title in purple.
            pywikibot.output(u"\n\n>>> \03{lightpurple}%s\03{default} <<<"
                             % page.title())
            # show what was changed
            pywikibot.showDiff(page.get(), text)
            pywikibot.output(u'Comment: %s' %comment)
            try:
                # Save the page
                page.put(text, comment=comment,
                    minorEdit=minorEdit, botflag=botflag)
                return True
            except pywikibot.LockedPage:
                pywikibot.output(u"Page %s is locked; skipping."
                                 % page.title(asLink=True))
            except pywikibot.EditConflict:
                pywikibot.output(
                    u'Skipping %s because of edit conflict'
                    % (page.title()))
            except pywikibot.SpamfilterError, error:
                pywikibot.output(
                    u'Cannot change %s because of spam blacklist entry %s'
                    % (page.title(), error.url))
            
        return False

def main():
    # This factory is responsible for processing command line arguments
    # that are also used by other scripts and that determine on which pages
    # to work on.
    genFactory = pagegenerators.GeneratorFactory()
    # The generator gives the pages that should be worked upon.
    gen = None
    # This temporary array is used to read the page title if one single
    # page to work on is specified by the arguments.
    pageTitleParts = []
    # If dry is True, doesn't do any real changes, but only show
    # what would have been changed.
    dry = False

    # Parse command line arguments
    for arg in pywikibot.handleArgs():
        if arg.startswith("-dry"):
            dry = True
        else:
            # check if a standard argument like
            # -start:XYZ or -ref:Asdf was given.
            if not genFactory.handleArg(arg):
                pageTitleParts.append(arg)

    if pageTitleParts != []:
        # We will only work on a single page.
        pageTitle = ' '.join(pageTitleParts)
        page = pywikibot.Page(pywikibot.getSite(), pageTitle)
        gen = iter([page])

    if not gen:
        gen = genFactory.getCombinedGenerator()
    if gen:
        # The preloading generator is responsible for downloading multiple
        # pages from the wiki simultaneously.
        gen = pagegenerators.PreloadingGenerator(gen)
        bot = BasicBot(gen, dry)
        bot.run()
    else:
        pywikibot.showHelp()

if __name__ == "__main__":
    try:
        main()
    finally:
        pywikibot.stopme()
