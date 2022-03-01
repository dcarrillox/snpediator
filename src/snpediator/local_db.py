import sqlite3
from sqlite3 import Error


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
                                        reference TEXT
                                    ); """

    sql_create_genotypes_table = """ CREATE TABLE IF NOT EXISTS genotypes_db (
                                            id integer IDENTITY PRIMARY KEY,
                                            rsid text,
                                            magnitude TEXT NOT NULL,
                                            color TEXT,
                                            summary TEXT
                                        ); """

    try:
        c = conn.cursor()
        c.execute(sql_create_columns_table)
        c.execute(sql_create_genotypes_table)
    except Error as e:
        print(e)

def insert_in_tables(conn, rsid_columns, rsid_genotypes):


    columns_values = (rsid_columns[column] for column in rsid_columns)
    sql_insert_columns = ''' INSERT INTO columns_db(rsid,gene,chr,position,reference)
                                VALUES(?,?,?,?,?) '''

    genotypes_values = (rsid_genotypes[genotype] for genotype in rsid_genotypes)
    sql_insert_genotypes = ''' INSERT INTO genotype_db(rsid,magnitude,color,summary)
                                    VALUES(?,?,?,?) '''

    with conn:
        cur = conn.cursor()
        cur.execute(sql_insert_columns, columns_values)
        cur.execute(sql_insert_genotypes, genotypes_values)

def check_isin_table(conn, rsid):

    sql_isin_table = ''' SELECT count(*) FROM columns_db WHERE rsid == ?'''

    print(rsid)
    cur = conn.cursor()
    cur.execute(sql_isin_table, (rsid,))
    count = cur.fetchall() # returns [(0,)] or [(1,)]

    return False if count[0][0] == 0 else True



# db_file = "../../database/local_db"
#
#
# conn = create_connection(db_file)
# create_tables(conn)

