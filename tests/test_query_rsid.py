import pytest

from snpediator.query_rsid import (check_rsid_online,
                                   parse_snpedia_online,
                                   query_snpedia_online)

__author__ = "dcarrillox"
__copyright__ = "dcarrillox"
__license__ = "MIT"


def test_no_rsid_online():
    rsid = "xxxxx"
    assert query_snpedia_online(rsid) == False


def rsid_online():
    rsid = "rs104894370"
    columns, genotypes = query_snpedia_online(rsid)
    return False if columns != columns == {'gene': 'MYL2', 'chr': '12', 'position': '110919145', 'orientation': 'minus', 'reference': 'GRCh38 38.1/141'} or genotypes != {'(C;T)': {'magnitude': 6.2, 'color': '#ff8080', 'summary': 'Familial Hypertrophic Cardiomyopathy'}, '(T;T)': {'magnitude': 0.0, 'color': '#80ff80', 'summary': 'common in clinvar'}} else True

def test_rsid_online():
    rsid_online_query = rsid_online()
    assert rsid_online_query == True