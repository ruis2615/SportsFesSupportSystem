import psycopg2
from flask import current_app

# テスト環境用のDB
TEST_DB_USER = ""
TEST_DB_PASSWORD = ""
TEST_DB_IP = ""
TEST_DB_PORT = 5432
TEST_DB_NAME = ""

# 号口環境用のDB
STABLE_DB_USER = ""
STABLE_DB_PASSWORD = ""
STABLE_DB_IP = ""
STABLE_DB_PORT = 5432
STABLE_DB_NAME = ""

def db_connect():
    if current_app.config.get("RUN_MODE") == 1:
        DATABASE_URL = f"postgresql://{TEST_DB_USER}:{TEST_DB_PASSWORD}@{TEST_DB_IP}:{TEST_DB_PORT}/{TEST_DB_NAME}"
        msg = "開発環境用のデータベースに接続しました。"
    else:
        DATABASE_URL = f"postgresql://{STABLE_DB_USER}:{STABLE_DB_PASSWORD}@{STABLE_DB_IP}:{STABLE_DB_PORT}/{STABLE_DB_NAME}"
        msg = "本番環境用のデータベースに接続しました。"
    connector = psycopg2.connect(DATABASE_URL)
    connector.set_client_encoding('utf-8')
    print(msg)
    return connector


class GetData:
    @staticmethod
    def get_fetchone(sql, *args):
        db_connector = db_connect()
        db_cursor = db_connector.cursor()
        db_cursor.execute(sql, args)
        result = db_cursor.fetchone()
        db_cursor.close()
        db_connector.close()
        return result

    @staticmethod
    def get_fetchall(sql, *args):
        db_connector = db_connect()
        db_cursor = db_connector.cursor()
        db_cursor.execute(sql, args)
        result = db_cursor.fetchall()
        db_cursor.close()
        db_connector.close()
        return result

    @staticmethod
    def get_fetchmany(sql, *args):
        db_connector = db_connect()
        db_cursor = db_connector.cursor()
        db_cursor.execute(sql, args)
        result = db_cursor.fetchmany()
        db_cursor.close()
        db_connector.close()
        return result


class SQL:
    @staticmethod
    def sql(sql):
        db_connector = db_connect()
        db_cursor = db_connector.cursor()
        db_cursor.execute(sql)
        db_connector.commit()
        db_cursor.close()
        db_connector.close()
        return