# FastAPI app to demonstrate API and Database interaction

Overview
--------
This [fastapi](https://fastapi.tiangolo.com/) python app creates a series of GET, POST, PUT, and DELETE endpoints capable of manipulating coupled data from a PostgresSQL database. 

The app was created based on the following user story.
#### User Story
As an API User, I want to be able to perform CRUD (Create, Read, Update, and Delete) operations on a group of tables representing part of a supply chain. These tables are:
- Products
- Orders
- Organisations

There will be some relationships between the tables e.g. Orders will be tied to Organisations.

App Requirements
------------
In order to be able to use this app we have a few requirements:
- [Docker](https://docs.docker.com/engine/install/)
- [Docker Compose](https://docs.docker.com/compose/install/)
- [Python 3.11](https://www.python.org/downloads/release/python-3110/)
- [Poetry](https://python-poetry.org/docs/)
- [Postman](https://www.postman.com/) app if you use the [postman collection](Products_and_Supplies_API.postman_collection.json) provided.
- A browser if you want to play around with the Swagger UI
- The database used is [PostgreSQL](https://www.postgresql.org/)
- [SQLAlchemy](https://www.sqlalchemy.org/) is the ORM used and [alembic](https://alembic.sqlalchemy.org/en/latest/) carries out the database migrations (see [helper readme](src/database/alembic/README) for more details).

Everything else will be installed in the docker images and there are execution commands detailed below.

:information_source: Strictly speaking you don't need Poetry to setup your local Python environment.

Build and Test
------------
### Python environment setup

If you want to use poetry to manage your local python environment please run the following commands

```bash
poetry config virtualenvs.in-project true
poetry install
```

this will configure poetry to create the virtual environment in the project directory and then install the virtual environment.  

If you aren't using poetry you can use the [`requirements.txt`](requirements.txt) file and your preferred python 
virtual environment manager to install all the required packages.

### Code Formatting

We use:
- [Black](https://github.com/psf/black) to format our code
- [isort](https://pycqa.github.io/isort/) to arrange module imports
- [flake8](https://flake8.pycqa.org/en/latest/) for code style analysis
- [mypy](https://mypy.readthedocs.io/en/stable/) for type-checking code analysis

To run `black`, `flake8`, and `mypy` locally you can use the individual scripts in the `bin` directory. 
Or you can run all four formatters together using
```bash
make lint
```

:information_source: Note this will reformat all Python code in your `src/` and `tests/` folders.
### Docker images setup

For this app we need a single docker images for the [app](Dockerfile).

We can build the image using the following docker-compose command
```bash
docker-compose build
```
:information_source: If you're using docker-compose v2+ you can use `docker compose build` instead but both commands work.

Now that we have the docker images all set, we can run/start them as containers
```bash
docker-compose up -d
```

If you want to build the images and start the containers with the same command you can use `docker-compose up -d --build`.

We can now check the logs to see if everything is ok using the following

```bash
docker-compose logs webapi
```

To check that everything is working as expected we can run some python tests using

```bash
docker-compose exec webapi python -m pytest
```

The Postgres database is currently live and public as an [AWS RDS](https://aws.amazon.com/rds/) instance. The URI is in the [docker-compose.yml](docker-compose.yml) file. The test database is used during local testing and is rolled back after each session. The "prod" database is live and populated with some data. CI spins up a local (to CI) Postgres database, then the migrations are applied before it is used to run the integrations tests in CI (Github Actions are currently being used for this).

Running the application
-------------------

If you executed the `docker-compose up -d` command already then the app. There is no need to initialise the database. 
If not, execute the command.

When the app is running (you can check the logs to make sure everything is up `docker-compose logs -f webapi`) you can check out the swagger UI 
by clicking [http://localhost:8004/docs#/](http://localhost:8004/docs#/). Here you'll see all the CRUD endpoints available. Or you can use the [postman collection](Products_and_Supplies_API.postman_collection.json) provided. 

### Products table
- 2x GET endpoints: one to retrieve a single record by it's unique ID and the other to retrieve many records (you can add how many records you'd like to skip or how many records you'd like to be returned). The return schema for a single product entry is `{"Category": "string", "Variety": "string", "Packaging": "string", "id": int}`.
- 1x POST endpoint: creates a new Product entry using the following schema: `{"Category": "string", "Variety": "string", "Packaging": "string"}`
- 1x PUT endpoint: updates an existing entry using the same schema as the POST endpoint with all optional fields. The entry ID must be provided to use PUT.
- 1x DELETE endpoint: deletes an existing field given the entry ID.

### Organisations table
- 2x GET endpoints: one to retrieve a single record by it's unique ID and the other to retrieve many records (you can add how many records you'd like to skip or how many records you'd like to be returned). The return schema for a single organisation entry is `{"Name": "string", "Type": Optional[enum("BUYER", "SELLER")], "id": int, "Orders": List[Orders], "Products": List[Products]}`.
- 1x POST endpoint: creates a new Organisation entry using the following schema: `{"Name": "string", "Type": enum("BUYER", "SELLER")}`
- 1x PUT endpoint: updates an existing entry using the same schema as the POST endpoint with all optional fields. The entry ID must be provided to use PUT.
- 1x DELETE endpoint: deletes an existing field given the entry ID.

### Orders table
- 2x GET endpoints: one to retrieve a single record by it's unique ID and the other to retrieve many records (you can add how many records you'd like to skip or how many records you'd like to be returned). The return schema for a single orders entry is `{"Type": enum("BUY", "SELL"), "Reference": int, "Products": List[Products], "Organisation_id": int, "id": int}`.
- 1x POST endpoint: creates a new Order using the following schema: `{"Type": enum("BUY", "SELL"), "Reference": Optional[int], "Products": Optional[List[Products]], "Organisation_id": int}`
- 1x PUT endpoint: updates an existing entry using the same schema as the POST endpoint with all optional fields. The entry ID must be provided to use PUT.
- 1x DELETE endpoint: deletes an existing field given the entry ID.

The schema for a single `Product` from the `Orders` table is
`{"Category": "mango", "Variety": "from orders", "Packaging": "18kg pallet", "Volume": "1 ton", "Price_per_unit": "1000 $/kg"}`. 

Once you're finished with the app you can shut everything down by running
```bash
docker-compose down
```

Future developments
----------

Aside from the above, there are other improvements that are required to ensure it is production-level. A few of these 
are highlighted below.
1. More test coverage, particularly for CRUD failure paths and edge cases.
2. There's definitely some more validation that needs to occur and there's more endpoints that are needed to increase the user experience which I've not really included. There are a few `todo`'s here and there in the code for some of these.
3. I have ignored any Auth in this app. For two reasons, one: I'm not that familiar with auth and I don't have much time to deep dive into it, and two: there isn't any sensitive data being passed around by the app, so it's probably ok with no auth for local usage. 
4. I've added basic continuous integration but no continuous deployment. Currently, I install python, the poetry environment, perform some code linting, run pytest, and build the docker image. Ideally, we'd want to run a few steps in CI: BUILD-STAGE: build-python, ensure code is of good standard with linters, and build docker images; TEST-STAGE: run python tests and ensure everything works as expected; and the DEPLOY-STAGE: push docker images to some repository e.g. AWS ECR. 
5. The API app runs locally at the moment but it would be great if it ran in the cloud and was automatically deployed with each successful MR/PR.
6. An optional frontend for an easier user experience.
7. Database access is currently very open, so in a real environment this would be a BIG no-no but similarly to auth - there isn't anything sensitive in the app or database and I'll take the database down soon enough. 