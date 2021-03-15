from builders.golang_builder import GolangBuilder
from builders.vue_builder import VueBuilder


# 获取构造器工具类


def get_builder(name, options=None):
    builder_map = {
        "go": create_go_builder,
        "vue": create_vue_builder
    }

    method = builder_map.get(name)
    if method:
        return method(options)
    return None


# 创建golang的构造器
def create_go_builder(options):
    return GolangBuilder(options)


# 创建vue的构造器
def create_vue_builder(options):
    return VueBuilder(options)
