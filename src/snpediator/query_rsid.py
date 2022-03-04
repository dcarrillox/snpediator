from bs4 import BeautifulSoup
import requests


def check_rsid_online(rsid):

    rsid = rsid.capitalize()

    url = "https://bots.snpedia.com/index.php"
    rsid_url = f"{url}/{rsid}"

    page = requests.get(rsid_url)
    soup = BeautifulSoup(page.content, "html.parser")

    # target text meaning the rsid is not in snpedia online
    target = "There is currently no text in this page."

    # identify p blocks
    ps = soup.findChildren("p")

    for p in ps:
        if target in p.getText():
            return False
    return True

def translate_color(page_color):
    if page_color == "#ff8080":
        return "red"
    elif page_color == "#80ff80":
        return "green"
    else:
        return "white"

def parse_snpedia_online(soup, rsid):
    rsid = rsid.capitalize()

    trs = soup.findChildren("tr")


    columns = {"rsid":rsid,
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
                    columns["gene"] = tds[index + 1].getText().strip()
                if td.getText() == "Reference":
                    columns["reference"] = tds[index + 1].getText()
                if td.getText() == "Chromosome":
                    columns["chr"] = tds[index + 1].getText()
                if td.getText() == "Position":
                    columns["position"] = int(tds[index + 1].getText())

                a = td.find("a")
                if a:
                    title = a.get('href')
                    geno = title.replace(f"/index.php/{rsid}", "")
                    if f"/index.php/{rsid}(" in title:

                        if geno not in genotypes:
                            genotypes[geno] = {"magnitude": str(), "color": str(), "summary": str()}
                            page_magnitude = tds[index + 1].getText().strip()
                            genotypes[geno]["magnitude"] = float(page_magnitude) if page_magnitude else "NaN"
                            page_color = tds[index + 1].get("style").split(" background: ")[1].strip()
                            genotypes[geno]["color"] = translate_color(page_color)
                            genotypes[geno]["summary"] = tds[index + 2].getText().strip()

    return columns, genotypes

def query_snpedia_online(rsid):
    """


    @param soup:
    @param rsid:
    """

    rsid = rsid.capitalize()
    url = "https://bots.snpedia.com/index.php"
    rsid_url = f"{url}/{rsid}"

    page = requests.get(rsid_url)
    soup = BeautifulSoup(page.content, "html.parser")

    columns, genotypes = parse_snpedia_online(soup, rsid)

    return columns, genotypes




