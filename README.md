su -c "createuser hzbu;createdb -h localhost -p 5432 -E UTF8 -O hzbu hzbdb;" - postgres


# Start the app locally 

```bash
uvicorn main:app --reload  
```

Deploy to heroku with the following

```bash
git push origin main
```

# Run DB Migrations with alembic

```bash
alembic revision --autogenerate -m "migration message"
alembic upgrade head
```

To run the migrations on heroku, run the following command

```bash
export ALCHEMY_DB_URL="postgresql://hzbu:password@localhost/hzbdb"  # Set the database url
```

# Run tests

```bash
pytest tests
```

# Run Locally 

```bash
virtualenv venv -p python3.13
. ./venv/bin/activate
pip install -r requirements.txt
```
 