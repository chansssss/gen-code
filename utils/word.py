def word2hump(word):
    resp = ""
    arr = word.split('_')
    for str in arr:
        resp = resp + str.title()
    return resp


if __name__ == '__main__':
    print(word2hump('create_at'))
