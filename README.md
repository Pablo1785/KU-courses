# DIS Project

## Starting the application
* STEP 1: Install `docker` and `docker-compose`, this may need a restart of your system since Docker is a very low level program.
* STEP 2: Run `docker-compose up` as either a user with permissions to docker, or with `sudo`/`doas`
* STEP 3: ???
* STEP 4: PROFIT!!!
The build process may take a while since it is both building a Java program, as well as the Python scraper which is quite large in the number of required dependencies. When built, the scraper will be one of the first things to run and it may take up to 30 minutes to finish scraping since we want to be nice to KU's surprisingly fragile IT infrastructure.

The entire application is governed through the `docker-compose.yml` file
present in the root directory. This file specifies each service we spin up, 
and makes these available to eachother on the internal network `dis-network`.
To spin the containers up simply run:

### PgAdmin
We've included a container running PgAdmin to provide a GUI for interacting 
with our relational data. By default it will be started up on port 5050.

At first run, it won't automatically connect to the postgres instance. To 
connect to it right click on 'servers' in the left navbar and select
register -> server. In the pop-up give it a name, and then navigate to the 
connection panel, here set the host name to equal the container name,
in our case "disku_pgdb" (as seen in the docker-compose), and point it at 
port 5432. Remember to provide it with the credentials "admin" "admin", such
that it gains access. You should now be ready to go!.

### Extracting files from PgAdmin
To extract the queries from the docker container, create a directory called queries, and run the following command:
```
sudo docker cp <docker_container_id>:/var/lib/pgadmin/storage/admin_private.org/. queries/
```
OBS: only the first few characters (3 or 4) of the id is nescessary.
The container id can be found via:

```
sudo docker ps -a
```

Conversely to import queries run the command in reverse (assuming the queries
you want to import are in /queries):

```
sudo docker cp queries/. <docker_container_id>:/var/lib/pgadmin/storage/admin_private.org/
```
Alternatively you can run one of two bash scripts `docker_export_script.sh` that extracts the queries from the docker container or `docker_import_script.sh` that imports the queries to the container. Both need the container id to be provided as a command line argument. 
#### Initialize database
After starting up the container containing the database, simply running `db-manager -f` will populate the database, optionally also launching it with the flag `-s` will cause the server to automatically start scraping webpages.

#### Visualizing database schema
You can do a nifty visualization by right clicking on "postgres" under "databases"
and choosing "ERD for database".
