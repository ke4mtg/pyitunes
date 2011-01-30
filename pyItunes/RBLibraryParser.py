import os
import xml.etree.cElementTree as ElementTree
import pyItunes as itunes
NEEDED_KEYS= set(("title", "genre", "artist", "album", "track-number", "location", "duration", "file-size", ))

class RBLibraryParser:
    def __init__(self,xmlLibrary):
        self.dictionary = self.parser(xmlLibrary)
    
    def _lookup_string(self,string, strmap):
        """Look up @string in the string map,
        and return the copy in the map.

        If not found, update the map with the string.
        """
        string = string or ""
        try:
            return strmap[string]
        except KeyError:
            strmap[string] = string
            return string

    def parser(self, dbfile, typ="song", keys=NEEDED_KEYS):
        """Return a list of info dictionaries for all songs
        in a Rhythmbox library database file, with dictionary
        keys as given in @keys.
        """
        
        rhythmbox_dbfile = os.path.expanduser(dbfile)

        lSongs = {}
        strmap = {"title":"Name","artist":"Artist","album":"Album","genre":"Genre","track-number":"Track Number","location":"Location","file-size":"Size","duration":"Total Time"}

        # Parse with iterparse; we get the elements when
        # they are finished, and can remove them directly after use.
        i=0

        for event, entry in ElementTree.iterparse(rhythmbox_dbfile):
            if not (entry.tag == ("entry") and entry.get("type") == typ):
                continue
            info = {}
            for child in entry.getchildren():
                if child.tag in keys:
                    tag = self._lookup_string(child.tag, strmap)
                    text = self._lookup_string(child.text, strmap)
                    if tag:
                        info[tag] = text
            lSongs[i]= info
            i+=1
            entry.clear()
        return lSongs
