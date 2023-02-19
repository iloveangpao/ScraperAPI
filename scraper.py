from requests_html import HTMLSession

class Scraper():
    def scrapedata(self,url):
        s = HTMLSession()
        r = s.get(url)
        print(r.status_code)

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