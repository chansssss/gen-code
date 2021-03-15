from db_utils.postgres_drive import PostgresDrive


# 获取构造器工具类
def get_db_drive(db_lang):
    db_drive_map = {
        "postgres": create_postgres_drive,
        "mysql": create_mysql_drive
    }

    method = db_drive_map.get(db_lang)
    if method:
        return method()
    return None


# 创建golang的构造器
def create_postgres_drive():
    return PostgresDrive()


# 创建vue的构造器
def create_mysql_drive():
    return PostgresDrive()
