# Shortest path

## Prerequisites

#### Neo4j

- Download & Run new4j
- create a database from the desktop app and proviede a password
- chage `GRAPHDB_USERNAME` & `GRAPHDB_PASSWORD` in `settings.py` to match your db username and password
- By default unit tests use the same database as the development one.To change this please change `TESST_GRAPHDB_USERNAME` &  `TEST_GRAPHDB_PASSWORD` in `settings.py`

#### Install python dependencies

- pip install -r requirements.txt

#### Prepare

```
python manage.py migrate
python manage.py clear_neo4j
python manage.py install_labels
```

## Run API server

```
python manage.py runserver
```

## API

- POST `/node/create/{name}` create node
- POST `/node/connect/{from}/{to}` connect 2 nodes
- GET `/node/path/{start}/{end}` shortest path between 2 nodes 

## Run Unit tests

- Test file : `node/test_nodes.py`
- Run Tests `python manage.py test`
- Test shortest path explained
    - ![](./docs/graph.jpg)
    - (1) shortpath = `a,j,k,l,m,i`
    - (2) connect `(n)` to `(c)` , shortpath = `a,b,c,n,i`
    - (3) disconnect `(n)` & `(c)`, shortpath = `a,j,k,l,m,i`
    - (4) connect `(e)` & `(n)`, shortpath = `a,j,k,l,m,i`
    - (5) disconnect `(e)` & `(n)` & connect `(d)` & `(n)`, shortpath =  `a,j,k,l,m,i` or `a,b,c,d,n,i`
    - (6) disconnect `(k)` & `(l)` shortpath = `a,b,c,d,n,i`


