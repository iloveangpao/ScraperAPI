from requests_html import HTMLSession
from lxml.etree import tostring
import lxml.html
import requests
import cssselect

class AdRemover(object):

    def __init__(self, *rules_files):
        if not rules_files:
            raise ValueError("one or more rules_files required")

        translator = cssselect.HTMLTranslator()
        rules = []

        for rules_file in rules_files:
            with open(rules_file, 'r') as f:
                for line in f:
                    # elemhide rules are prefixed by ## in the adblock filter syntax
                    if line[:2] == '##':
                        try:
                            rules.append(translator.css_to_xpath(line[2:]))
                        except cssselect.SelectorError:
                            # just skip bad selectors
                            pass

        # create one large query by joining them the xpath | (or) operator
        self.xpath_query = '|'.join(rules)


    def remove_ads(self, tree):

        for elem in tree.xpath(self.xpath_query):
            elem.getparent().remove(elem)


class Scraper():

    def adBlock(self,url):
        rule_urls = ['https://easylist-downloads.adblockplus.org/ruadlist+easylist.txt',
                    'https://filters.adtidy.org/extension/chromium/filters/1.txt']

        rule_files = [url.rpartition('/')[-1] for url in rule_urls]

        # download files containing rules
        for rule_url, rule_file in zip(rule_urls, rule_files):
            r = requests.get(rule_url)
            with open(rule_file, 'w') as f:
                print(r.text, file=f)


        remover = AdRemover(*rule_files)

        html = requests.get(url).text
        document = lxml.html.document_fromstring(html)
        remover.remove_ads(document)
        clean_html = tostring(document).decode("utf-8")

        return clean_html

    def scrapedata(self,url):
        r = self.adBlock(url)

        qlist = []

        quotes = r.html.find('p')

        for q in quotes:
            item = {
                'text': q.text.strip()
            }
            qlist.append(item)
        return qlist

quotes = Scraper()

quotes.scrapedata('life')