Working with csv & excel is not convenient for effective queries.
In this repository structural variations (sv) data transformed into the sql tables.

## Before run
Fill the **application.properties** file to connect to the database

#### PSQL setup Mac Os:
installation

`brew install postgres`

starting server

`pg_ctl -D /usr/local/var/postgres start`

set environment variable before calling `psql ${DB_NAME}`

`PGPASSWORD=${PASSWORD} psql -U ${USER_NAME} ${DB_NAME}`

## Resources
https://dcc.icgc.org/releases/PCAWG/consensus_sv
https://dcc.icgc.org/releases/PCAWG/donors_and_biospecimens

Look wiki for more details:
https://github.com/Timoniche/PCAWG_SQL/wiki