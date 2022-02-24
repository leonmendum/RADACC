# Server

create youre own .enx file

```Bash
cp ./packages/backend/.env.example ./packages/backend/.env
```

synchronize the database

```docker-compose
docker-compose exec backend npm run typeorm schema:sync
```

load some sample data

```docker-compose
docker-compose exec backend npm run fixtures
```
