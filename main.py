import argparse
import yaml

from gen_code import GenCode


def load_config(path):
    # 由于官方提示load方法存在安全漏洞，所以读取文件时会报错。加上warning忽略，就不会显示警告
    yaml.warnings({'YAMLLoadWarning': False})
    f = open(path, 'r', encoding='utf-8')  # 打开yaml文件
    cfg = f.read()
    d = yaml.load_all(cfg)  # 将数据转换成python字典行驶输出，存在多个文件时，用load_all，单个的时候load就可以
    print(d)
    for data in d:
        return data


parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('-c', '--conf', dest='config', default=None,
                    help='sum the integers (default: find the max)')
if __name__ == '__main__':
    args = parser.parse_args()

    if args.config:
        # load_config(args.config)
        genCode = GenCode(load_config(args.config))
        genCode.gen_code()

# from jinja2 import Environment, FileSystemLoader
#
#
#
# env = Environment(loader=FileSystemLoader('.'))
# template = env.get_template('template.go')
# print(template.render(name='demo'))
