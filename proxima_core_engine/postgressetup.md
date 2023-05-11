psql postgres

DROP DATABASE proximacoreenginedb;

CREATE DATABASE proximacoreenginedb;

ALTER USER proximaadmin WITH SUPERUSER;


CREATE USER proximaadmin WITH PASSWORD 'aTgLpUfKGhu';
GRANT ALL PRIVILEGES ON DATABASE proximacoreenginedb TO proximaadmin;
ALTER ROLE proximaadmin SET client_encoding TO 'utf8';
ALTER ROLE proximaadmin SET default_transaction_isolation TO 'read committed';
ALTER ROLE proximaadmin SET timezone TO 'UTC';

docker run --name postgresql-container -p 5432:5432 -e POSTGRES_PASSWORD=aTgLpUfKGhu -d postgres
psql -h localhost -p 5432 -U postgres -W