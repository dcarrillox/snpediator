import sqlite3
from sqlite3 import Error
from termcolor import colored, cprint


def create_connection(db_file):

    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn

def create_tables(conn):

    sql_create_columns_table = """ CREATE TABLE IF NOT EXISTS columns_db (
                                        rsid TEXT PRIMARY KEY,
                                        gene TEXT,
                                        chr TEXT NOT NULL,
                                        position INTEGER NOT NULL,
                                        orientation TEXT NOT NULL,
                                        reference TEXT
                                    ); """

    sql_create_genotypes_table = """ CREATE TABLE IF NOT EXISTS genotypes_db (
                                            id integer PRIMARY KEY AUTOINCREMENT,
                                            rsid TEXT,
                                            genotype TEXT NOT NULL,
                                            magnitude REAL,
                                            color TEXT,
                                            summary TEXT
                                        ); """

    try:
        c = conn.cursor()
        c.execute(sql_create_columns_table)
        c.execute(sql_create_genotypes_table)
    except Error as e:
        print(e)

def insert_in_tables(conn, rsid, rsid_columns, rsid_genotypes):

    rsid = rsid.capitalize()

    columns_values = [rsid_columns[column] for column in rsid_columns]
    print(columns_values)
    sql_insert_columns = ''' INSERT INTO columns_db(rsid,gene,chr,position,orientation,reference)
                                VALUES(?,?,?,?,?,?) '''

    with conn:
        cur = conn.cursor()
        cur.execute(sql_insert_columns, columns_values)

        
    # insert multiple genotypes
    for genotype in rsid_genotypes:
        genotype_values = [rsid_genotypes[genotype][feature] for feature in rsid_genotypes[genotype]]
        genotype_values.insert(0, genotype)
        genotype_values.insert(0, rsid)

        print(genotype_values)
        sql_insert_genotypes = ''' INSERT INTO genotypes_db(rsid,genotype,magnitude,color,summary)
                                        VALUES(?,?,?,?,?) '''

        with conn:
            cur.execute(sql_insert_genotypes, genotype_values)

            
def check_isin_table(conn, rsid):
    rsid = rsid.capitalize()

    sql_isin_table = ''' SELECT count(*) FROM columns_db WHERE rsid == ?'''

    print(rsid)
    cur = conn.cursor()
    cur.execute(sql_isin_table, (rsid,))
    count = cur.fetchall() # returns [(0,)] or [(1,)]

    return False if count[0][0] == 0 else True


def get_rsid_from_table(conn, rsid):
    to_print = {"genotypes":dict()}

    sql_rsid_columns = """SELECT * FROM columns_db WHERE rsid == ? """
    cur = conn.cursor()
    cur.execute(sql_rsid_columns, (rsid,))
    columns = cur.fetchall()[0]

    features = ["rsid", "gene", "chr", "position", "orientation", "reference"]
    for feature, column in zip(features, columns):
        to_print[feature] = column


    sql_rsid_genotypes = """SELECT * FROM genotypes_db WHERE rsid == ? """
    cur = conn.cursor()
    cur.execute(sql_rsid_genotypes, (rsid,))
    genotypes = cur.fetchall()

    features = ["magnitude", "color", "summary"]
    for genotype in genotypes:
        genotype_alleles = genotype[2]
        to_print["genotypes"][genotype_alleles] = dict()
        for feature, value in zip(features, genotype[3:]):
            to_print["genotypes"][genotype_alleles][feature] = value

    return to_print

def print_rsid(to_print):

    cprint(f"\t{to_print['rsid']}\t", attrs=["bold", "underline"])
    # gene
    cprint("\t", end=""), cprint(f"- Gene: ", attrs=["bold"], end=""), cprint(to_print['gene'], end="")
    # orient
    cprint("\t", end=""), cprint(f"- Orient: ", attrs=["bold"], end=""), cprint(to_print['orientation'], end="")
    # genotype_1


