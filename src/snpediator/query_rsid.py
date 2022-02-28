from bs4 import BeautifulSoup
import requests


def check_rsid_presence(soup):

    # target text meaning the rsid is not in snpedia online
    target = "There is currently no text in this page."

    # identify p blocks
    ps = soup.findChildren("p")

    for p in ps:
        if target in p.getText():
            return False
    return True

def parse_snpedia_online(soup, rsid):

    trs = soup.findChildren("tr")

    columns = {"rsid":str(),
               "gene":str(),
               "chr":str(),
               "position":int(),
               "orientation":str(),
               "reference":str()
               }
    genotypes = dict()

    trs = soup.findChildren("tr")
    for tr in trs:
        tds = tr.findChildren("td")
        if tds:
            for index, td in enumerate(tds):
                if td.getText() == "Stabilized":
                    columns["orientation"] = tds[index + 1].getText()
                if td.getText() == "Gene":
                    columns["gene"] = tds[index + 1].getText()
                if td.getText() == "Reference":
                    columns["reference"] = tds[index + 1].getText()
                if td.getText() == "Chromosome":
                    columns["chr"] = tds[index + 1].getText()
                if td.getText() == "Position":
                    columns["position"] = tds[index + 1].getText()

                a = td.find("a")
                if a:
                    title = a.get('href')
                    geno = title.replace(f"/index.php/{rsid}", "")
                    if f"/index.php/{rsid}(" in title:
                        if geno not in genotypes:
                            genotypes[geno] = {"magnitude": str(), "color": str(), "summary": str()}
                            genotypes[geno]["magnitude"] = float(tds[index + 1].getText().strip())
                            genotypes[geno]["color"] = tds[index + 1].get("style").split(" background: ")[1].strip()
                            genotypes[geno]["summary"] = tds[index + 2].getText().strip()

    return columns, genotypes

def query_snpedia_online(rsid: str) -> str:
    """
    Queries the rsid at https://bots.snpedia.com/index.php.
    If there is a page for the rsid, returns a BeautifulSoup object with it,
    otherwise it returns None.

    @param rsid:
    """

    url = "https://bots.snpedia.com/index.php"
    rsid_url = f"{url}/{rsid}"

    page = requests.get(rsid_url)
    soup = BeautifulSoup(page.content, "html.parser")

    # check if the rsid is online
    is_online =  check_rsid_presence(soup)

    if is_online:
        columns, genotypes = parse_snpedia_online(soup, rsid)
        print(columns)
        print(genotypes)
    else:
        return False



rsid = "Rs104894370"


query_snpedia_online(rsid)
