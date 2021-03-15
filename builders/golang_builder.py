from jinja2 import Environment, FileSystemLoader

# golang 的构造器
from utils.word import word2hump


class GolangBuilder():
    def __init__(self, options):
        self.web_frame = options['web']
        self.orm_frame = options['orm']
        self.env = Environment(loader=FileSystemLoader('./builders/templates/golang'))
        self.env.filters['word2hump'] = word2hump
        self.web_template = None
        self.orm_template = None
        self.domain_template = None

    def generate(self, entities):
        self._set_template()
        for entity in entities:
            file = open('{}.go'.format(entity['name']), mode='w')
            file.write(self.web_template.render(name=entity['name'], columns=entity['columns']))
            break

    def _set_template(self):
        self.web_template = self.env.get_template('template_web_{}.go'.format(self.web_frame))
        # self.orm_template = self.env.get_template('template_orm_{}.go'.format(self.orm_frame))
        # self.domain_template = self.env.get_template('template_domain_{}.go'.format(self.web_frame))
