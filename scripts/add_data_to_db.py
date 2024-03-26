import sqlalchemy

from npi_grants.readers import grants, npi

engine = sqlalchemy.create_engine('sqlite:///data/grant_npi.db')
conn = engine.connect()


greader = grants.GrantReader('data/RePORTER_PRJ_C_FY2022.csv')
greader.to_db(conn)

nreader = npi.NPIReader('data/pl_pfile_20050523-20240211.csv')
nreader.to_db(conn)

