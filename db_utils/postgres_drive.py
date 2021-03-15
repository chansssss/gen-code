class PostgresDrive:
    def __init__(self):
        self.protocol = 'postgresql'
        self.entities = []
        self.types = None

    def db_table_2_entity(self, tables):
        for table in tables:
            temps = []
            for column in table['columns']:
                temp = {"name": column['name'], "type": self._get_type(column['type'])[0],
                        'len': self._get_type(column['type'])[1]}
                temps.append(temp)
            self.entities.append({"name": table["name"], "columns": temps})
        return self.entities

    def _get_type(self, db_type):
        str_type = str(db_type)
        if str_type.startswith('VARCHAR'):
            return 'string', db_type.length
        if str_type.startswith('TIMESTAMP WITH TIME ZONE'):
            return 'date', 0
        if str_type.startswith('INTEGER'):
            return 'int', 0
        if str_type.startswith('BOOLEAN'):
            return 'bool', 0
        if str_type.startswith('TEXT'):
            return 'text', db_type.length
        return 'string'
