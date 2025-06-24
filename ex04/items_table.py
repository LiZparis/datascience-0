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
    # df = pd.read_csv(csv_path)
    # .csv文件太大最好流式写入版本（不 concat
    dtype_map = {
        "product_id": types.Integer(),
        "category_id": types.BigInteger(),
        "category_code": types.String(255),
        "brand": types.String(255)  # 或 sqlalchemy.UUID(as_uuid=True) 如果你愿意
    }
    try:
        for chunk in pd.read_csv(csv_path, chunksize=10000):
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

    path = "../../subject/item/item.csv"  # 修改为你实际路径
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
