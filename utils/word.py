import inflect

p = inflect.engine()


def word2hump(word):
    resp = ""
    arr = word.split('_')
    for str in arr:
        resp = resp + str.title()
    return resp


# 转单数
def singular(word):
    resp = ""
    arr = word.split('_')
    for index, str in enumerate(arr):
        if p.singular_noun(str):
            str = p.singular_noun(str)
        if index == 0:
            resp = str
        else:
            resp = resp + "_" + str
    return resp


# 转单数加首字母小写
def singular_and_flmbl(word):
    resp = ""
    arr = word.split('_')
    for index, str in enumerate(arr):
        if p.singular_noun(str):
            str = p.singular_noun(str)
        if index == 0:
            resp = resp + str
        else:
            resp = resp + str.title()
    return resp


# 转单数加驼峰写法
def singular_and_title(word):
    resp = ""
    arr = word.split('_')
    for str in arr:
        if not p.singular_noun(str):
            resp = resp + str.title()
            continue
        resp = resp + p.singular_noun(str).title()
    return resp
