import configparser

from authentication import Authentication
from endpoint import Endpoint
from sql import SQL
from sql_table import define_table, metadata

config = configparser.ConfigParser()
config.read('requests_configuration.ini')

auth = {}
endpoints = dict()
sql = None
tables = dict()
raw_tables = dict()

for section in config.sections():
    if section == 'Authentication':
        auth = Authentication(**config[section])
    elif section == 'SQL':
        sql = SQL(**config[section])
    elif section == 'News':
        raw_tables[section] = config[section]
    else:
        endpoints[section] = Endpoint(section, **config[section])

for name, tbl in raw_tables.items():
    columns = dict(**tbl)
    del columns['__key__']
    tables[name] = define_table(sql.engine(), name, tbl['__key__'], **columns)

metadata.create_all(sql.engine())

for endpoint in endpoints.values():
    endpoint.run(auth, sql.session(), tables)
