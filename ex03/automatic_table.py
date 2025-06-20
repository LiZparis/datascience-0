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
    print(f"{csv_path} is loading to {table_name}...")
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
    print(f"✅ table {table_name} finishe loading")

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

    customer_dir = "/goinfre/lzhang2/subject/customer"  # 修改为你实际路径

    for filename in os.listdir(customer_dir):
        if filename.endswith(".csv"):
            csv_path = os.path.join(customer_dir, filename)
            table_name = os.path.splitext(filename)[0]
        try:
            if not table_exists(engine, table_name):
                load_csv_to_postgres(engine, csv_path, table_name)
            else:
                print(f"⚠️ Table {table_name} already exists.")
        except Exception as e:
            print(f"❌ Failed to process {filename}: {e}")

    engine.dispose()
    print("✅ Process is finished")

if __name__ == "__main__":
    main()

# head -n 5 item.csv  
'''虽然用 Pandas + to_sql() 能自动建表并导入数据，但你一旦要做以下操作，就必须写 SQL：
场景	是否需要 SQL
精确控制字段类型、主键、索引	✅ 是的
创建多个表、外键关联	✅ 是的
执行复杂查询逻辑（JOIN、GROUP BY）	✅ 是的
建表前先检查/清空表	✅ 是的
控制权限、视图、函数等	✅ 是的
单纯读入 CSV 简单分析	❌ 可以只用 Pandas'''
'''CREATE TABLE IF NOT EXISTS items (
    product_id INTEGER,
    category_id BIGINT,
    category_code VARCHAR(255),
    brand VARCHAR(64)
);
'''
