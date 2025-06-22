import psycopg2
# PostgreSQL 官方推荐的 Python 驱动库之一。
# 它提供了标准的数据库连接、游标（cursor）、SQL 执行、事务处理等接口。


'''Docker + PostgreSQL 连接规则总结：
你在哪里运行 Python 脚本？	host 应该写什么？	port 需要写吗？	原因
✅ 容器内部（如 app）	"db"（服务名）	默认 5432 可省略	同一 Docker 网络中，服务名就是主机名
✅ 宿主机（如 VSCode 终端）	"localhost"	要写 5432	需要通过端口映射连接容器的 PostgreSQL'''
conn = psycopg2.connect(
    dbname="piscineds",
    user="lzhang2",
    password="mysecretpassword",
    # 容器外测试
    host="localhost",
    port="5432"
    # 容器内测试
    # host="db"
)

'''游标用于执行 SQL 语句；
本质上它是你和数据库对话的“会话窗口”；
所有的 execute(...) 都需要通过它来完成'''
cur = conn.cursor()

# 创建表
cur.execute("""
    CREATE TABLE IF NOT EXISTS students (
        id SERIAL PRIMARY KEY,
        name TEXT NOT NULL
    );
""")
# 对于 INSERT、UPDATE、DELETE、CREATE 这类 修改操作，一定要 commit 才能生效！
conn.commit()

# PostgreSQL 的序列相当于一个“票号机”，它只往前走，永远不会自动倒回。
# 清空数据并重置序列（可选）
cur.execute("DELETE FROM students;")
cur.execute("ALTER SEQUENCE students_id_seq RESTART WITH 1;")

# %s 是参数占位符，防止 SQL 注入；
# 参数要作为元组传入，如 ("Alice",)（即使是一个值也要加逗号）；
cur.execute("INSERT INTO students (name) VALUES (%s)", ("Alice",))
cur.execute("INSERT INTO students (name) VALUES (%s)", ("Bob",))
cur.execute("INSERT INTO students (name) VALUES (%s)", ("charlie",))
conn.commit()

# 查询数据
cur.execute("SELECT * FROM students;")
rows = cur.fetchall()
for row in rows:
    print(row)

# 清理资源
cur.close()
conn.close()
'''cur.close()：关闭游标；

conn.close()：关闭数据库连接；

⚠️ 不调用不会立刻出错，但会占用资源，是良好习惯。'''
