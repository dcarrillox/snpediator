import logging
import sys, os
import argparse
from platformdirs import *



from snpediator import __version__

from snpediator.local_db import *
from snpediator.query_rsid import *



__author__ = "dcarrillox"
__copyright__ = "dcarrillox"
__license__ = "MIT"

_logger = logging.getLogger(__name__)



def main():

    parser = argparse.ArgumentParser(description='')
    requiredArgs = parser.add_argument_group("Required Arguments")
    requiredArgs.add_argument('-r', '--rsid',
                              dest='rsid',
                              required=True,
                              help=''
                              )

    args = parser.parse_args()

    appname = "snpediator"
    appauthor = "dcarrillox"

    # init local_db

    db_path = user_data_dir(appname, appauthor)
    os.makedirs(db_path, exist_ok=True)
    db_file = db_path + "/snpediator_local.db"
    #os.remove(db_file)


    rsid = rsid.strip().capitalize()
    rsid = args.rsid.strip().capitalize()


    conn = create_connection(db_file)
    create_tables(conn)

    isin_table = check_isin_table(conn, rsid)


    if not isin_table:

        print()
        print("Querying SNPedia online...")
        # check if the rsid is available online
        is_online = check_rsid_online(rsid)

        if is_online:
            # query snpedia online
            rsid_columns, rsid_genotypes = query_snpedia_online(rsid)

            # insert results into the local_db
            insert_in_tables(conn, rsid, rsid_columns, rsid_genotypes)

        else:
            print("rsid not found.")
            sys.exit()

    else:
        print()
        print(f"{rsid} already in local_db, reading from it...")


    to_print = get_rsid_from_table(conn, rsid)
    print_rsid(to_print)



if __name__ == "__main__":
    main()


