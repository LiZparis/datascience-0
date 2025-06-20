import pandas as pd
import os
from sqlalchemy import create_engine, MetaData
import sqlalchemy.types as types
# pip install sqlalchemy
# pip install pandas psycopg2-binary


def table_exists(engine, table_name):
    metadata = MetaData()
    metadata.reflect(bind=engine)
    return table_name in metadata.tables

def load_csv_to_postgres(engine, csv_path, table_name):
    print(f"{csv_path}is loading to {table_name}...")
    df = pd.read_csv(csv_path)

    # 明确设置字段类型，符合“6种数据类型”要求
    dtype_map = {
        "event_time": types.DateTime(),
        "event_type": types.String(length=255),
        "product_id": types.Integer(),
        "price": types.Float(),
        "user_id": types.BigInteger(),
        "user_session": types.String(length=64)  # 或 sqlalchemy.UUID(as_uuid=True) 如果你愿意
    }

    df["event_time"] = pd.to_datetime(df["event_time"])
    df.to_sql(table_name, engine, index=False, dtype=dtype_map)
    print(f"✅ Table {table_name} finishe loading")

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

    path = "/goinfre/lzhang2/subject/customer/data_2022_oct.csv"  # 修改为你实际路径
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