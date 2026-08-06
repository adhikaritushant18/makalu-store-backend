# Makalu Store Backend Ops

This guide covers the most useful PostgreSQL, auth, and Docker commands for the FastAPI backend.

## 1. Important Current Behavior

Admin login does **not** use the `users` table.

The active login endpoint checks only these backend environment variables:

- `ADMIN_USERNAME`
- `ADMIN_PASSWORD`

Code reference:
- `app/auth/router.py`

That means:

- changing rows in `users` will **not** change admin login
- to change admin login, update backend `.env` and restart/redeploy the backend

## 2. Check Running Containers

List running containers:

```bash
docker ps -a
```

Show only Compose services from the backend project:

```bash
cd /home/ubuntu/makalustore.com/backend
docker compose ps
```

## 3. Enter PostgreSQL

Open a shell in the Postgres container:

```bash
docker exec -it makalu-store-postgres sh
```

Start `psql` from inside the container:

```bash
psql -U postgres -d makalu-store
```

Or connect directly from the host in one command:

```bash
docker exec -it makalu-store-postgres psql -U postgres -d makalu-store
```

## 4. Useful psql Commands

List databases:

```sql
\l
```

Show current connection info:

```sql
\conninfo
```

List schemas:

```sql
\dn
```

List tables in current schema:

```sql
\dt
```

List only app tables in `public`:

```sql
\dt public.*
```

Describe a table:

```sql
\d users
\d assignments
\d equipments
```

Show first 10 rows from a table:

```sql
SELECT * FROM users LIMIT 10;
SELECT * FROM categories LIMIT 10;
SELECT * FROM equipments LIMIT 10;
```

Exit `psql`:

```sql
\q
```

Reset a broken multi-line command in `psql`:

```sql
\r
```

## 5. Check Database Contents

List all user tables:

```sql
SELECT table_schema, table_name
FROM information_schema.tables
WHERE table_schema = 'public'
ORDER BY table_name;
```

Count rows in important tables:

```sql
SELECT COUNT(*) FROM users;
SELECT COUNT(*) FROM categories;
SELECT COUNT(*) FROM locations;
SELECT COUNT(*) FROM equipments;
SELECT COUNT(*) FROM assignments;
SELECT COUNT(*) FROM partners;
```

Check Alembic migration version:

```sql
SELECT * FROM alembic_version;
```

## 6. Backend Auth Commands

Check backend env values used for login:

```bash
docker exec -it makalu-store-backend env | grep -E "ADMIN_USERNAME|ADMIN_PASSWORD|DATABASE_URL|CORS_ORIGINS|ROOT_PATH"
```

Test local backend root:

```bash
curl -i http://localhost:8000/
```

Test admin login directly against FastAPI:

```bash
curl -i -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  --data "username=reservationmakalu&password=Ma@kalu11058925"
```

Test public login through Nginx `/api`:

```bash
curl -i -X POST "https://store.makalutour.com/api/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  --data "username=reservationmakalu&password=Ma@kalu11058925"
```

Test `/auth/me` with a token:

```bash
curl -i "http://localhost:8000/auth/me" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

## 7. Why Frontend Login May Show No Network Request

If browser DevTools shows no request during login, check these first:

1. The Network panel may be filtered.
   Example: if the filter box contains text like `blog`, unrelated requests are hidden.

2. The request may be blocked before sending because of browser-side JavaScript error.

3. The frontend may not have been redeployed after env/code changes.

4. The frontend may be pointing at the wrong API URL.

For this project, frontend should use:

```env
NEXT_PUBLIC_API_URL=https://store.makalutour.com/api
```

## 8. How to Check the Real Admin Login Credentials

Because admin login uses env vars, check them with:

```bash
docker exec -it makalu-store-backend env | grep -E "ADMIN_USERNAME|ADMIN_PASSWORD"
```

If you want to update them, edit backend `.env`:

```bash
cd /home/ubuntu/makalutour.com/backend
vim .env
```

Then restart backend:

```bash
docker compose down
docker compose up --build -d
```

## 9. How to Create a User Row in PostgreSQL

This creates a row in the `users` table, but it does **not** enable admin login in the current code.

Open `psql`:

```bash
docker exec -it makalu-store-postgres psql -U postgres -d makalu-store
```

Insert a user:

```sql
INSERT INTO users (username, password, role)
VALUES ('marketingmakalu@gmail.com', 'plain-text-password', 'manager');
```

See created users:

```sql
SELECT id, username, role FROM users ORDER BY id;
```

Delete a user:

```sql
DELETE FROM users
WHERE username = 'marketingmakalu@gmail.com';
```

Update a user password:

```sql
UPDATE users
SET password = 'new-password'
WHERE username = 'marketingmakalu@gmail.com';
```

## 10. Important Warning About Users

The `users` table currently stores plain-text passwords and is not wired into the active admin auth flow.

So:

- you can create rows there for data purposes
- those rows will not let you log into `/auth/login`
- to make DB-backed users work, the backend auth code must be changed to query `users`

## 11. Backend Logs

See backend logs:

```bash
docker logs makalu-store-backend --tail 200
```

Follow backend logs live:

```bash
docker logs -f makalu-store-backend
```

See Postgres logs:

```bash
docker logs makalu-store-postgres --tail 200
```

## 12. Docs / Proxy Checks

Check local FastAPI docs:

```bash
curl -i http://localhost:8000/docs
curl -i http://localhost:8000/openapi.json
```

Check public docs through Nginx:

```bash
curl -i https://store.makalutour.com/api/docs
curl -i https://store.makalutour.com/api/openapi.json
```

If `/api/docs` loads but `/openapi.json` is requested instead of `/api/openapi.json`, set backend `ROOT_PATH=/api`.

## 13. Frontend Deployment Checks

Check current frontend containers:

```bash
docker ps -a
```

Check if the frontend is using the right env in its deployment system:

```env
NEXT_PUBLIC_API_URL=https://store.makalutour.com/api
```

If frontend is containerized and rebuilt locally:

```bash
docker compose up -d --build
```

## 14. Most Useful One-Line Commands

Show backend login env:

```bash
docker exec -it makalu-store-backend env | grep -E "ADMIN_USERNAME|ADMIN_PASSWORD|DATABASE_URL"
```

Open Postgres:

```bash
docker exec -it makalu-store-postgres psql -U postgres -d makalu-store
```

List tables:

```bash
docker exec -it makalu-store-postgres psql -U postgres -d makalu-store -c "\dt public.*"
```

Test local login:

```bash
curl -i -X POST "http://localhost:8000/auth/login" -H "Content-Type: application/x-www-form-urlencoded" --data "username=reservationmakalu&password=Ma@kalu11058925"
```

Test public login:

```bash
curl -i -X POST "https://store.makalutour.com/api/auth/login" -H "Content-Type: application/x-www-form-urlencoded" --data "username=reservationmakalu&password=Ma@kalu11058925"
```
