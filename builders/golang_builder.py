import os
import pathlib
from jinja2 import Environment, FileSystemLoader
from utils.word import word2hump, singular, singular_and_title, singular_and_flmbl


# golang 的构造器
class GolangBuilder():
    def __init__(self, options):
        # 初始化参数
        self.web_frame = options['web']
        self.orm_frame = options['orm']
        self.web_output = options['web_output']
        self.orm_output = options['orm_output']
        self.protocol_output = options['protocol_output']
        # 注册过滤器
        self.env = Environment(loader=FileSystemLoader('./builders/templates/golang'))
        self.env.filters['word2hump'] = word2hump
        self.env.filters['singular'] = singular
        self.env.filters['singular_and_flmbl'] = singular_and_flmbl
        self.env.filters['singular_and_title'] = singular_and_title
        # 初始化template
        self.web_template = None
        self.orm_template = None
        self.protocol_template = None

    # 生成函数
    def generate(self, entities):
        from builders import includes, excludes
        self._set_template()
        for entity in entities:
            is_gen = True
            if includes:
                if entity['name'] in includes:
                    is_gen = True
                else:
                    is_gen = False
            if excludes:
                if entity['name'] in excludes:
                    is_gen = False
                else:
                    is_gen = True
            if is_gen:
                self._gen_code_file(self.web_output, entity, self.web_template, "handler_")
                self._gen_code_file(self.orm_output, entity, self.orm_template, "")
                self._gen_code_file(self.protocol_output, entity, self.protocol_template, "protocol_")

    # 设置template
    def _set_template(self):
        self.web_template = self.env.get_template('template_web_{}.go'.format(self.web_frame))
        self.orm_template = self.env.get_template('template_orm_{}.go'.format(self.orm_frame))
        self.protocol_template = self.env.get_template('template_protocol_{}.go'.format(self.web_frame))
        pathlib.Path(self.web_output).mkdir(parents=True, exist_ok=True)
        pathlib.Path(self.orm_output).mkdir(parents=True, exist_ok=True)
        pathlib.Path(self.protocol_output).mkdir(parents=True, exist_ok=True)

    def _gen_code_file(self, output, entity, template, prefix):
        file = open(os.path.join(output, ('{}{}.go'.format(prefix, singular(entity['name'])))), mode='w')
        file.write(template.render(name=entity['name'], columns=entity['columns']))
