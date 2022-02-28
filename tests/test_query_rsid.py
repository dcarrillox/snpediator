import pytest

from snpediator.query_rsid import check_rsid_presence, parse_snpedia_online, query_snpedia_online

__author__ = "dcarrillox"
__copyright__ = "dcarrillox"
__license__ = "MIT"


def test_no_rsid_online():
    rsid = "xxxxx"
    assert query_snpedia_online(rsid) == False



