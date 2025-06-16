# 使用 Docker 搭建 PostgreSQL 数据库并连接（42 Piscine DataScience 项目）

## 🐳 第一步：编写 `docker-compose.yml`

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

## 🔧 第二步：处理 Docker 权限（WSL）

若 `docker info` 提示权限错误：

```
permission denied while trying to connect to the Docker daemon socket
```

请执行以下命令（在 Ubuntu 中）：

```bash
sudo usermod -aG docker li
```

然后在 **Windows PowerShell 中**运行：

```powershell
wsl --shutdown
```

再重新打开 Ubuntu，确保用户已加入 `docker` 用户组：

```bash
id
# 输出中应包含：docker
```

## 🚀 第三步：启动 PostgreSQL 容器

```bash
cd datascience-0/ex00/
docker compose up -d
```

## 🛠 第四步：安装 `psql` 工具（本地命令行客户端）

```bash
sudo apt update
sudo apt install postgresql-client
```

## 🔗 第五步：连接 PostgreSQL 容器

```bash
psql -U lzhang2 -d piscineds -h localhost -W
```

输入密码：`mysecretpassword`

成功后你会看到：

```
psql (14.18 ...)
Type "help" for help.
```

## 🧪 第六步：SQL 测试命令

```sql
-- 查看当前数据库有哪些表
\l              -- 查看数据库列表
\c piscineds    -- 连接数据库（你已经在里面了）
\dt             -- 查看数据表（如果还没建会为空）

-- 创建测试表
CREATE TABLE test_users (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL
);

-- 插入数据
INSERT INTO test_users (name) VALUES ('li'), ('docker'), ('postgres');

-- 查询数据
SELECT * FROM test_users;
```

## ⚠️ 常见问题

### Q1. `psql: command not found`

→ 没安装 `psql`，请执行：

```bash
sudo apt install postgresql-client
```

---

### Q2. `permission denied while trying to connect to the Docker daemon socket`

→ 当前用户没有加入 `docker` 组，请参照上文解决。

---

### Q3. `Did not find any relations.`

→ 数据库中还没有表。请先 `CREATE TABLE`。

---

完成以上步骤，你就能成功使用 Docker 部署并连接 PostgreSQL！