# 📘 42 校区无 sudo 权限完成 Chapter III - Exercise 00 的 PostgreSQL 部署指南

---

## 🎯 题目要求回顾

| 要求 | 内容 |
|------|------|
| 数据库名称 | `piscineds` |
| 用户名 | 你的 42 登录名（如 `lzhang2`） |
| 密码 | `mysecretpassword` |
| 启动环境 | 若校区有 PostgreSQL 可用，直接使用；否则需用 Docker Compose |
| 提交内容 | 无需上传文件；助教通过 `psql` 命令连接测试 |
| 测试命令 | `psql -U your_login -d piscineds -h localhost -W` |

---

## 🐳 使用 Docker Compose 启动 PostgreSQL（推荐）

### 1️⃣ 创建 `docker-compose.yml` 文件（放在 `ex00/` 目录）

请将 `POSTGRES_USER` 替换为你的 42 登录名：

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

volumes:
  pgdata:
```

---

### 2️⃣ 启动容器

进入 `ex00/` 目录后运行：

```bash
docker compose up -d
```

等待容器启动成功，出现 `Started` 提示。

---

### 3️⃣ 无法使用 `psql`？用容器内的客户端连接：

因为校区不能 sudo 安装 `psql`，我们改为在容器内连接：

```bash
docker exec -it ex00-db-1 psql -U lzhang2 -d piscineds
```

效果和 `psql -U ... -h localhost` 是一样的。

---

## ✅ 助教将如何测试你配置是否正确？

他们会运行如下命令：

```bash
psql -U lzhang2 -d piscineds -h localhost -W
```

如果你的容器仍在运行、配置无误、监听 `localhost:5432`，他们就能成功连接。

---

## 🧪 可选：容器内测试 SQL（建议演示）

```sql
CREATE TABLE hello42 (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL
);

INSERT INTO hello42 (name) VALUES ('li'), ('docker');

SELECT * FROM hello42;
```

---

## 🛠 常见问题与解决方法

### ❓ `psql: command not found`

→ 无法安装 `psql`，请改用：

```bash
docker exec -it ex00-db-1 psql -U lzhang2 -d piscineds
```

---

### ❓ 助教无法连接？

- 容器是否启动中？用 `docker ps` 确认；
- `docker-compose.yml` 中端口是否映射为 `"5432:5432"`？
- 用户名、密码是否严格为题目要求？

---

## ✅ 总结

你不需要 sudo，也不需要本机装 PostgreSQL。只要 Docker 可用，就能完成全部要求，并通过助教的测试命令连接。