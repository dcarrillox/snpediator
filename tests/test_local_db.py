import os
import shutil

from snpediator.local_db import (create_connection,
                                 create_tables,
                                 insert_in_tables,
                                 check_isin_table)


__author__ = "dcarrillox"
__copyright__ = "dcarrillox"
__license__ = "MIT"



def test_set_database():
    ## set database directory
    db_dir = "tests/database_test"
    db_file = f"{db_dir}/local_db_test"
    os.makedirs(db_dir, exist_ok=True)

    # create db
    conn = create_connection(db_file)
    # create tables
    create_tables(conn)
    # check random rsid in table
    rsid = "not an rsid at all"
    isin_table = check_isin_table(conn, rsid)

    assert isin_table == False

def test_insert_rsid():
    ## set database directory
    db_dir = "tests/database_test"
    db_file = f"{db_dir}/local_db_test"
    # connect to db
    conn = create_connection(db_file)

    rsid = "rs1051730"
    rsid_columns = {'rsid': 'Rs1051730', 'gene': 'CHRNA3', 'chr': '15', 'position': 78601997, 'orientation': 'minus', 'reference': 'GRCh38 38.1/142'}
    rsid_genotypes = {'(C;C)': {'magnitude': 2.0, 'color': '#80ff80', 'summary': 'Smokes normal (lower) number of cigarettes if a smoker.'}, '(C;T)': {'magnitude': 2.0, 'color': '#ff8080', 'summary': '1.3x increased risk of lung cancer'}, '(T;T)': {'magnitude': 2.5, 'color': '#ff8080', 'summary': '1.8x increased risk of lung cancer; reduced response to alcohol, therefore possibly increased risk of alcohol abuse'}}

    insert_in_tables(conn, rsid, rsid_columns, rsid_genotypes)

    # check if the rsid is in the table
    isin_table = check_isin_table(conn, rsid)

    assert isin_table == True
