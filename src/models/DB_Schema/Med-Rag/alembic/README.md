# Run Alembic Migrations

## Config
```bash
cp alembic.ini.example alembic.ini
```
- Update the `alembic.ini` with your database credentials(`sqlalcheny.url`)

### create new migrations

```bash
alembic revision --autogenerate -m "Add .."
```

### Use this command to upgrade the database

```bash
alembic upgrade head
```