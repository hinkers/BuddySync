import configparser

from dotenv import dotenv_values

from apisync.web.api import Api
from container import container
from apisync.scripts.custom_script import CustomScript
from apisync.web.endpoint import Endpoint
from apisync.database.sql import SQL
from apisync.database.sql_table import define_table


def read_config(filenames):
    env = dotenv_values(".env")

    config = configparser.RawConfigParser()
    config.optionxform = str
    
    raw_tables = dict()
    one_to_many = dict()
    one_to_one = dict()
    run = dict()

    for filename in filenames:
        with open(filename, 'r') as config_file:
            config_string = config_file.read()
            for v_name, v_value in env.items():
                config_string = config_string.replace(f'${{{v_name}}}', v_value)
            config.read_string(config_string)

    for section in config.sections():
        if section == 'Authentication':
            api = Api(**config[section])
        elif section == 'SQL':
            container.sql = SQL(**config[section])
        elif section == 'Relationships:OneToMany':
            one_to_many = dict(**one_to_many, **config[section])
        elif section == 'Relationships:OneToOne':
            one_to_one = dict(**one_to_one, **config[section])
        elif section == 'Run':
            run = dict(**run, **config[section])
        elif section == 'Scripts':
            container.scripts = dict(
                **container.scripts,
                **{
                    name: CustomScript(s_name)
                    for name, s_name in config[section].items()
                }
            )
        elif ':' in section:
            s_type, s_name = section.split(':', 1)
            if s_type == 'Table':
                raw_tables[s_name] = config[section]
            elif s_type == 'Endpoint':
                container.endpoints[s_name] = Endpoint(s_name, **config[section])
            else:
                raise KeyError(f"Unknown section type '{section}'")
        else:
            raise KeyError(f"Unknown section type '{section}'")

    container.sql.add_relationships('one_to_many', one_to_many)
    container.sql.add_relationships('one_to_one', one_to_one)

    for name, tbl in raw_tables.items():
        columns = dict(**tbl)
        del columns['__key__']
        container.tables[name] = define_table(container.sql, name, tbl['__key__'], columns)

    container.sql.create_tables()

    for endpoint in container.endpoints.values():
        endpoint.api = api

    if len(run) > 0:
        for e_name, count in run.items():
            if e_name.startswith('Script:'):
                container.scripts[e_name[7:]].run()
            else:
                for _ in range(int(count)):
                    container.endpoints[e_name].run()
    else:
        for endpoint in container.endpoints.values():
            endpoint.run()
