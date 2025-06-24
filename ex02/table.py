import pandas as pd
import os
from sqlalchemy import create_engine, MetaData
from sqlalchemy.dialects.postgresql import UUID
import sqlalchemy.types as types
# pip install sqlalchemy
# pip install pandas psycopg2-binary


def table_exists(engine, table_name):
    metadata = MetaData()
    metadata.reflect(bind=engine)
    return table_name in metadata.tables


def load_csv_to_postgres(engine, csv_path, table_name):
    print(f"{csv_path}is loading to {table_name}...")
    # df = pd.read_csv(csv_path)
    # .csv文件太大最好流式写入版本（不 concat
    dtype_map = {
            "event_time": types.DateTime(),
            "event_type": types.String(length=255),
            "product_id": types.Integer(),
            "price": types.Float(),
            "user_id": types.BigInteger(),
            # 将 user_session 存为真正的 UUID 类型
            "user_session": UUID(as_uuid=True)
            # "user_session": types.String(length=64) 这种写法对将 user_session 存为普通字符串，最多64字符
        }
    try:
        for chunk in pd.read_csv(csv_path, chunksize=10000):
            # ⏳ 转换日期格式，非法时间会变成 NaT
            chunk["event_time"] = pd.to_datetime(chunk["event_time"], errors="coerce")

            # ✅ 插入数据库，流式写入，防止内存占满
            chunk.to_sql(
                table_name,
                engine,
                index=False,
                if_exists="append",  # 每块追加，不要覆盖
                dtype=dtype_map
            )
        print(f"✅ Table {table_name} finished loading.")

    except Exception as e:
        print(f"❌ Failed to process {table_name}: {e}")


def main():
    # user = "lzhang2"
    # password = "mysecretpassword"
    # host = "localhost"
    # port = "5432"
    # dbname = "piscineds"
    # table_name = "data_2022_oct"
    # path = "../../../../goinfre/subject/customer/data_2022_oct.csv"
    # create_engine(f"postgresql://{user}:{password}@{host}:{port}/{dbname}")
    db_url = "postgresql://lzhang2:mysecretpassword@localhost:5432/piscineds"
    engine = create_engine(db_url)
    path = "../../subject/customer/data_2022_oct.csv"
    # path = "/goinfre/lzhang2/subject/customer/data_2022_oct.csv"
    table_name = os.path.splitext(os.path.basename(path))[0]
    try:
        if not table_exists(engine, table_name):
            load_csv_to_postgres(engine, path, table_name)
        else:
            print(f"⚠️ Table {table_name} already exists, skipping.")
    except Exception as e:
        print(f"❌ Error while loading {table_name}: {e}")
    finally:
        engine.dispose()


if __name__ == "__main__":
    main()

'''当你使用 SQLAlchemy.create_engine(...) 创建数据库连接引擎时，它实际上会在内部维持一个连接池（connection pool），以便复用连接、提高效率。

而 engine.dispose() 的作用是：

    🔧 强制关闭并清空所有连接池中的连接，释放底层数据库资源。'''
'''什么是 UUID？
格式如下（共 36 个字符，包括 4 个连字符）：
bcd560a2-9c99-4ff2-848b-e4c1a3035809
它由五段组成：8-4-4-4-12，总共 32 个十六进制数字 + 4 个破折号。'''
