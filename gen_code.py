import json

import builders
from builders import get_builder, includes
from sqlalchemy import create_engine, inspect

from db_drive import get_db_drive


class GenCode:
    def __init__(self, yaml):
        self.config = GenConfig().parse(yaml)
        self.tables = []
        self.entities = None
        self.back_end_builder = None
        self.front_end_builder = None
        self._create_builder()
        self._set_tables()

    def _create_db_drive(self):
        self.db_drive = get_db_drive(self.config.db_lang)

    def _create_builder(self):
        self.back_end_builder = get_builder(self.config.back_end_lang,
                                            {"web": self.config.back_end_web,
                                             "orm": self.config.back_end_orm,
                                             "web_output": self.config.output['handler'],
                                             "protocol_output": self.config.output['protocol'],
                                             "orm_output": self.config.output['model'],
                                             })
        self.front_end_builder = get_builder(self.config.front_end_lib)

    def _set_tables(self):
        if self.config.resource_type == 'sql':
            self._get_table_for_db()
        else:
            self._get_table_for_json()

    def _get_table_for_db(self):
        self._create_db_drive()
        sql_url = "{}://{}:{}@{}:{}/{}".format(self.db_drive.protocol, self.config.db_username,
                                               self.config.db_password,
                                               self.config.db_host, self.config.db_port,
                                               self.config.db_database)
        engine = create_engine(sql_url)
        # 创建DBSession类型:
        # DBSession = sessionmaker(bind=engine)
        inspector = inspect(engine)
        schemas = inspector.get_schema_names()

        for schema in schemas:
            for table_name in inspector.get_table_names(schema=schema):
                columns = []
                if table_name.startswith('sql_'):
                    continue
                for column in inspector.get_columns(table_name, schema=schema):
                    columns.append(column)
                self.tables.append({"name": table_name, "columns": columns})
        self.entities = self.db_drive.db_table_2_entity(self.tables)

    def _get_table_for_json(self):
        self.entities = json.loads(self.config.json_dir)

    def gen_code(self):
        self.back_end_builder.generate(self.entities)
        # self.front_end_builder.generate(self.entities)


resource_types = ['sql', 'json']


class GenConfig:
    def __init__(self):
        self.resource_type = "sql"
        self.db_lang = ""
        self.db_host = ""
        self.db_username = ""
        self.db_password = ""
        self.db_port = ""
        self.db_database = ""
        self.json_dir = ""
        self.back_end_lang = "go"
        self.back_end_web = ""
        self.back_end_orm = ""
        self.front_end_lib = "vue"
        self.front_end_ui = "element"

        self.output = {
            'ui': '',
            'control': '',
            'domain': '',
            'dao': ''
        }

    def parse(self, yaml):
        try:
            self.resource_type = yaml["table_resource"]["type"]
            if "includes" in yaml["table_resource"]:
                builders.includes = yaml["table_resource"]["includes"].split(",")
            if "excludes" in yaml["table_resource"]:
                builders.excludes = yaml["table_resource"]["excludes"].split(",")
        except:
            raise Exception('缺少table_resouce type,且可选值为sql或者json')
        if self.resource_type not in resource_types:
            raise Exception('table_resouce type可选值为sql或者json')
        try:
            if self.resource_type == 'sql':
                self.db_lang = yaml["table_resource"]["db"]["lang"]
                self.db_host = yaml["table_resource"]["db"]["host"]
                self.db_username = yaml["table_resource"]["db"]["username"]
                self.db_password = yaml["table_resource"]["db"]["password"]
                self.db_port = yaml["table_resource"]["db"]["port"]
                self.db_database = yaml["table_resource"]["db"]["database"]
            else:
                self.json_dir = yaml["db"]["database"]
            self.back_end_lang = yaml["frame"]["lang"]
            self.back_end_web = yaml["frame"]["web"]
            self.back_end_orm = yaml["frame"]["orm"]
            self.front_end_lib = yaml["frame"]["front_lib"]
            self.front_end_ui = yaml["frame"]["ui"]

            self.output = {
                'view': yaml["output"]["view"],
                'handler': yaml["output"]["handler"],
                'protocol': yaml["output"]["protocol"],
                'model': yaml["output"]["model"]
            }
        except:
            raise Exception('参数配置文件有误，请检查后再运行。')
        return self
