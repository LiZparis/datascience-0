
# 📘 42 校区无 sudo 权限完成 Chapter III - Exercise 00 的 PostgreSQL 部署指南

## 🎯 题目要求回顾

| 要求       | 内容                              |
|------------|-----------------------------------|
| 数据库名称 | `piscineds`                       |
| 用户名     | 你的 42 登录名（如 `lzhang2`）     |
| 密码       | `mysecretpassword`                |
| 启动环境   | 使用 Docker Compose                |
| 提交内容   | 助教通过 `psql` 命令连接测试       |
| 测试命令   | `psql -U your_login -d piscineds -h localhost -W` |

---

## 🐳 使用 Docker Compose 启动 PostgreSQL（推荐）

### 1️⃣ 创建 `docker-compose.yml` 文件

```yaml
services:
  db:
    image: postgres:14
    environment:
      POSTGRES_USER: lzhang2
      POSTGRES_PASSWORD: mysecretpassword
      POSTGRES_DB: piscineds
    ports:
      - "5432:5432"
    volumes:
      - pgdata:/var/lib/postgresql/data

  pgadmin:
    image: dpage/pgadmin4
    environment:
      PGADMIN_DEFAULT_EMAIL: lzhang2@student.42.fr
      PGADMIN_DEFAULT_PASSWORD: mysecretpassword
    ports:
      - "8080:80"
    depends_on:
      - db

volumes:
  pgdata:
```

### 2️⃣ 启动容器

```bash
docker compose up -d
```

---

### 3️⃣ 如果无 psql，则容器内连接：

```bash
docker exec -it ex00-db-1 psql -U lzhang2 -d piscineds
```

---

## ✅ 助教测试连接方式

```bash
psql -U lzhang2 -d piscineds -h localhost -W
```

---

## 🧪 容器内测试 SQL（建议演示）

```sql
CREATE TABLE hello42 (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL
);
INSERT INTO hello42 (name) VALUES ('li'), ('docker');
SELECT * FROM hello42;
```

---

## 🛠 常见问题解决

### `psql: command not found`

→ 请改用容器内连接方式（见上）。

### 助教无法连接？

- 检查容器是否运行：`docker ps`
- 检查端口映射是否正确：5432:5432
- 用户名密码是否一致

---

# Data Science Project - PostgreSQL + Docker + PGAdmin

## 一、项目目标

* 使用 Docker 创建 PostgreSQL 数据库环境
* 使用 PGAdmin 可视化管理
* 用 Python 加载 CSV 数据至数据库
* 使用 SQLAlchemy / psycopg2 进行数据操作

---

## 二、项目实操记录

### 1. Python 加载 CSV 数据到 PostgreSQL

```python
import pandas as pd
import os
from sqlalchemy import create_engine
import sqlalchemy.types as types

db_url = "postgresql://lzhang2:mysecretpassword@localhost:5432/piscineds"
engine = create_engine(db_url)
df = pd.read_csv("item.csv")

dtype_map = {
    "product_id": types.Integer(),
    "category_id": types.BigInteger(),
    "category_code": types.String(length=255),
    "brand": types.String(length=64)
}
df.to_sql("items", engine, index=False, dtype=dtype_map)
engine.dispose()
```

---

### 2. 为何指定字段类型？

* 防止 `pandas` 猜错字段类型
* 提升数据库查询效率
* datetime 格式可做时间查询、统计

---

### 3. PGAdmin 使用说明

| 功能                        | 说明                       |
|-----------------------------|----------------------------|
| Tool > Query Tool           | 写 SQL 语句执行查询          |
| View/Edit Data              | 查看表格内容，类似 Excel     |
| Refresh                     | 新建数据或表后手动刷新       |

---

### 4. PostgreSQL CLI 命令

```sql
\l                      -- 查看所有数据库
\c piscineds           -- 连接数据库
\dt                    -- 查看所有表
DROP TABLE items;       -- 删除表
SELECT * FROM items;    -- 查看数据
```

---

## 三、SQLAlchemy vs psycopg2

### 🔹 psycopg2 是什么？

Python 原生 PostgreSQL 驱动。适合执行原始 SQL：

```python
import psycopg2
conn = psycopg2.connect(...)
cur = conn.cursor()
cur.execute("SELECT * FROM table")
rows = cur.fetchall()
```

优点：控制精细、性能高  
缺点：语法繁琐，需要手动管理连接

---

### 🔹 SQLAlchemy 是什么？

高级数据库封装库，可作为 ORM 或 Engine 使用：

```python
from sqlalchemy import create_engine
import pandas as pd
engine = create_engine("postgresql://...")
df.to_sql("table_name", engine, index=False)
```

优点：简单、和 pandas 配合好  
缺点：底层细节封装较多，不适合复杂 SQL

---

### 🔸 对比总结

| 比较点         | psycopg2     | SQLAlchemy                  |
|----------------|--------------|-----------------------------|
| 类型           | 驱动层        | 封装层 / ORM               |
| 操作           | 手写 SQL      | 自动建表，快速插入            |
| 适合场景       | 精细控制、大量 SQL | 快速数据导入、表结构生成      |
| 配合 pandas    | 不方便        | 非常方便                     |

---

## 四、项目建议

* ex00-ex02 可不设数据持久化
* ex03 建议加 volume 持久化数据
* PGAdmin 操作简便但功能有限
* 建议结合 SQLAlchemy 快速导入数据，复杂逻辑用 psycopg2 编写 SQL

---

如需继续设计图表、分析指标、JOIN 逻辑，欢迎随时继续。
