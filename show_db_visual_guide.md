# 📘 Chapter IV – Exercise 01：Show me your DB（图形化数据库查看）

---

## 🧾 题目要求总结

> • Find a way to visualize the db easily with a software  
> • The chosen software must help you to easily find and manipulate data using its own corresponding ID

---

## ❌ 不推荐工具：Prisma

虽然 Prisma 是一个强大的 ORM 工具，但它：

- 没有图形界面；
- 依赖 TypeScript/Node 项目环境；
- 不支持直接可视化表格、数据与结构；

🔴 **结论：不适用于本题。**

---

## ✅ 推荐工具：DBeaver（跨平台）

### 🔧 安装方法（本地或校区）

- Windows/macOS/Linux 都支持
- 官网下载：https://dbeaver.io/download/
- 或用 snap 安装（如果在 Linux）：
  ```bash
  sudo snap install dbeaver-ce
  ```

---

## 🐳 数据库准备（复用 ex00）

确保你在 `ex00/` 中已运行 PostgreSQL：

```bash
docker compose up -d
```

确认容器正在监听本地 5432 端口：

```bash
docker ps
```

---

## 🔗 在 DBeaver 中创建连接

1. 打开 DBeaver → 点击左上角 `New Database Connection`
2. 选择 `PostgreSQL` → 点击 Next
3. 配置连接参数：

| 参数 | 值 |
|------|----|
| Host | `localhost` |
| Port | `5432` |
| Database | `piscineds` |
| Username | `lzhang2` |
| Password | `mysecretpassword` |

4. 点击 **Test Connection** → 若提示驱动未安装，选择自动下载即可
5. 点击 Finish 保存连接

---

## 📊 可视化浏览数据

连接成功后你可以：

- 浏览数据库结构（表、列、约束等）
- 打开表并直接查看内容
- 用 SQL 编辑器执行查询（如 `SELECT * FROM test`）
- 使用图形界面过滤、排序、按 ID 查找数据

---

## ✅ 验收建议（演示时可以做）

- 展示你已连接数据库
- 展示一张表的结构与部分内容
- 按某一行 ID 搜索数据
- 可选：执行一个简单的 SQL 语句如 `SELECT * FROM test`

---

## ✅ 总结

| 项目要求 | 你的做法 |
|-----------|----------|
| 可视化数据库结构 | ✅ DBeaver |
| 查找数据并按 ID 查看 | ✅ 支持 |
| 容器化部署 PostgreSQL | ✅ docker compose |
| 图形界面易操作 | ✅ 鼠标点击即可操作所有数据 |

你现在可以自信地展示你的数据库，并满足项目的所有要求！