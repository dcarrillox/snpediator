import click
import logging
import pathlib
import sys
import argparse

from snpediator import __version__
from local_db import *
from query_rsid import *


__author__ = "dcarrillox"
__copyright__ = "dcarrillox"
__license__ = "MIT"

_logger = logging.getLogger(__name__)



def main():

    # parser = argparse.ArgumentParser(description='')
    # requiredArgs = parser.add_argument_group("Required Arguments")
    # requiredArgs.add_argument('-r', '--rsid',
    #                           dest='rsid',
    #                           required=True,
    #                           help=''
    #                           )
    #
    # args = parser.parse_args()



    # init local_db
    db_file = "../../database/local_db"

    rsid = "rs1051730 "
    rsid = rsid.strip().capitalize()


    conn = create_connection(db_file)
    create_tables(conn)

    isin_table = check_isin_table(conn, rsid)


    if not isin_table:

        # check if the rsid is available online
        is_online = check_rsid_online(rsid)

        if is_online:
            # query snpedia online
            rsid_columns, rsid_genotypes = query_snpedia_online(rsid)

            # insert results into the local_db
            insert_in_tables(conn, rsid, rsid_columns, rsid_genotypes)
    else:
        print(f"RSID {rsid} already in local_db, reading from it...")




if __name__ == "__main__":
    main()


# @click.group(context_settings=dict(help_option_names=["-h", "--help"]))
# @click.version_option(__version__)
# def cli():
#     """Run `snpediator COMMAND -h` for subcommand help"""
#     pass
#
#
# @cli.command()
# @click.argument("rsid", required=True, type=str)
# def query():
#     return rsid
#
# cli.add_command(query)
#
# cli()