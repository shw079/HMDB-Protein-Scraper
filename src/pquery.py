from urllib.request import urlopen
import re


class ProteinQuery:
    def __init__(self, query):
        self.query = query
        self._page = 1
        self._request = 'https://hmdb.ca/unearth/q?button=&query={}&searcher=proteins'.format(self.query)
        self.res = []

    def _next_page(self):
        self._page += 1
        self._request = 'https://hmdb.ca/unearth/q?button=&page={}&query={}&searcher=proteins'.format(self._page, self.query)

    def parse(self):
        page = urlopen(self._request)
        # flag to go to next page
        next = False
        for line in page:
            line = line.decode("utf-8")
            if line.startswith('  <a rel="next"'):
                next = True
            elif line.startswith('</div><div class="unearth-search-results unearth-protein-search-results">'):
                # parse search results
                matches = re.findall(">([a-zA-Z0-9_\\- ]+?)<", line)
                i = 0
                while i < len(matches):
                    if matches[i].startswith("HMDB"):
                        # HMDB and UniProt ID
                        record = [matches[i], matches[i+1].rstrip()]
                        i += 2
                    elif "metabolite" in matches[i]:
                        # protein name
                        record.append(matches[i+1])
                        self.res.append(record)
                        i += 2
                    else:
                        i += 1
                break
        page.close()
        if next:
            self._next_page()
            self.parse()