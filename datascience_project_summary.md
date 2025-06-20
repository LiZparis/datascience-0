
# 🧪 42 项目 DataScience 小总结（ex00 - ex04）

本笔记总结了本次项目练习中涉及到的 Docker + PostgreSQL + Python 数据导入与可视化流程。

---

## 📁 项目结构与练习目标

在 ex00 ～ ex02 中，我们主要学习：

- 如何构建 Docker 容器并运行 PostgreSQL；
- 如何使用 `pgAdmin4` 可视化数据库；
- 如何导入 CSV 数据到数据库中；
- 如何使用 Python 和 SQL 脚本查询数据库。

从 ex03 开始，我们：

- 实现了数据的 **自动化批量导入**；
- 开始使用 `SQLAlchemy` + `pandas` 实现数据清洗；
- 配合 `matplotlib` 做图表可视化。

---

## 🧰 使用的技术工具

| 技术组件   | 功能                     |
|------------|--------------------------|
| Docker     | 容器化数据库和 pgAdmin   |
| PostgreSQL | 数据库                   |
| pgAdmin4   | 可视化操作数据库         |
| pandas     | CSV 读取和处理           |
| SQLAlchemy | 与 PostgreSQL 建立连接   |
| psycopg2   | 执行 SQL 脚本、复杂查询 |
| matplotlib | 绘图展示分析结果         |

---

## 🧱 Docker 容器设计

- 在 ex00～ex02 中没有设置持久化；
- 从 ex03 开始使用 `volumes:` 实现数据持久化；
- 启动容器后使用 `pgAdmin` 进行连接与查看。

注意：

- `docker-compose.yml` 中不建议再写 `version` 字段（已过时）；
- 如果端口 `5432` 被占用，记得释放或改用其他端口。

---

## 📊 pgAdmin 使用技巧

- 初次连接要添加服务器（localhost + 对应端口）；
- `View/Edit Data` → `All Rows` 可查看表格内容；
- 如果表结构有更新，需右键 → `Refresh`；
- 每次刷新后可能会退出账户，需重新登录；
- 可以在 `Tools` → `Query Tool` 中运行 SQL；
- 数据筛选后可右键导出为 CSV。

---

## 📁 数据目录结构说明

```bash
$ ls -alR
customer/
  data_2022_oct.csv
  data_2022_nov.csv
  ...
items/
  items.csv
```

这些是待导入的原始数据（位于宿主机路径 `/goinfre/...`），并不代表数据库内的结构。数据导入后会在 PostgreSQL 中创建表。

---

## 💾 为什么需要定义数据类型？

虽然 Pandas 能自动导入数据，但为了符合要求（如 "6 种数据类型"），我们需要明确指定类型：

```python
dtype_map = {
    "event_time": types.DateTime(),
    "event_type": types.String(length=255),
    "product_id": types.Integer(),
    ...
}
```

此外：
- `event_time` 被强制转为 `pd.to_datetime()`，确保在 PostgreSQL 中是 `TIMESTAMP` 类型；
- 这不仅符合题目要求，也方便做时间过滤、图表分析等。

✅ 这属于数据清洗的一部分，**非常有用**。

---

## 🔄 SQLAlchemy vs psycopg2 区别详解

| 比较点             | psycopg2                     | SQLAlchemy                        |
|------------------|------------------------------|-----------------------------------|
| 类型             | 底层库（驱动）               | 高级库（封装引擎/ORM）           |
| 操作风格         | 手写 SQL，需管理事务         | 支持 ORM，也可用于快速插入       |
| 配合 pandas       | 不方便                        | `to_sql()`、`read_sql()` 直接用   |
| 用于复杂 SQL 查询 | ✅ 最佳选择                   | 可以写，但不如 psycopg2 灵活     |
| 推荐场景         | 精确查询、事务处理             | 快速导入、数据清洗分析           |

项目中常见应用：

- ✅ 数据导入：SQLAlchemy + pandas
- ✅ 数据查询、图表：psycopg2 + SQL 脚本

---

## 🔚 总结

项目的整体目标是让我们掌握：

- 数据库建表与数据导入（包括多表）；
- Python 脚本连接数据库；
- SQL 脚本查询、分析；
- 图表可视化；
- Docker 环境搭建与使用；
- `pgAdmin` 的基本操作。

掌握这套流程，对于未来从事数据分析、数据工程等职位非常有帮助 ✅

