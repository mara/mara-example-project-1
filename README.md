# Mara Example Project 1

A runnable app that demonstrates how to build a data warehouse with mara. 
Combines the [mara-pipelines](https://github.com/mara/mara-pipelines) and 
[mara-schema](https://github.com/mara/mara-schema) libraries 
with the [mara-app](https://github.com/mara/mara-app) framework into a project. 

The example ETL integrates publicly available e-commerce and marketing data into a more general 
modeling and structure for highlighting the capabilities of the Mara framework.

The repository is intended to serve as a template for new projects.

&nbsp;


## Getting started

### Sytem requirements

Python >=3.6 and PostgreSQL >=10 and some smaller packages are required to run the example (and mara in general). 

Mac:

```console
$ brew install -v python3
$ brew install -v dialog
$ brew install -v coreutils
$ brew install -v graphviz
```

Ubuntu 16.04:

```console
$ sudo apt install git dialog coreutils graphviz python3 python3-dev python3-venv
```

&nbsp;

Mara does not run Windows.

&nbsp;

On Mac, install Postgresql with `brew install -v postgresql`. On Ubuntu, follow  [these instructions](https://www.postgresql.org/download/linux/ubuntu/). 
Also, install the [cstore_fdw](https://github.com/citusdata/cstore_fdw) with `brew install cstore_fdw` and [postgresql-hll](https://github.com/citusdata/postgresql-hll) extensions from source.

To optimize PostgreSQL for ETL workloads, update your postgresql.conf along [this example](docs/postgresql.conf).

Start a database client with `sudo -u postgres psql postgres` and then create a user with `CREATE ROLE root SUPERUSER LOGIN;` (you can use any other name).

&nbsp;

### Installation

Clone the repository somewhere and hit `make` in the root directory of the project. This will:

- create a virtual environment in `.venv`,
- install all packages from [`requirements.txt.freeze`](requirements.txt.freeze) (if you want to create a new `requirements.txt.freeze` from [`requirements.txt`](requirements.txt), then run `make update-packages`),
- copy the file `app/local_setup.py.example` to `app/local_setup.py`, which you can adapt to your machine.
- create the necessary databases and a number of tables that are needed for running mara.
- store the Olist e-commerce and marketing data in the `olist_ecommerce` PostgreSQL database, locally.


You can now activate the virtual environment with 

```console
$ source .venv/bin/activate
```

To list all available flask cli commands, run `flask` without parameters.

&nbsp;

### Running the web UI

```console
$ flask run --with-threads --reload --eager-loading
```

The app is now accessible at [http://localhost:5000](http://localhost:5000).

&nbsp;

### Running the ETL

For development, it is recommended to run the ETL from the web UI (see above). 
On production, use `flask mara_pipelines.ui.run` to run a pipeline or a set of its child nodes. 

The command `mara_pipelines.ui.run-interactively` provides an ncurses-based menu for selecting and running pipelines.

&nbsp;

## Documentation

Documentation is work in progress. But the code base is quite small and documented.
