## Scribe

To clone the project, run:

```
git clone https://github.com/panalexeu/scribe_rag.git
```

## overview

Scribe is a locally hosted RAG web app that supports language and embedding models from multiple providers.

## server part

### dependencies

The server is fully written in python, hence it depends on the package manager. As the package manager, poetry was chosen, so to run the server, poetry must be installed.

### start-up

run:

```
cd ./scribe
```

then:

```
poetry install
```

to install all dependent packages. after that, you must activate the python shell with:

```
poetry shell
```

great, the only thing left is to simply run:

```
./start.sh
```

to start the server and chroma db.

### envs

To run the server, envs must be provided in the .env file:

- SCRIBE_DB - configure SQLite db type: dev - in-memory, prod - in-file.

### additional notes

Makefile stores commands to test and run the server

## ui-part

The UI is fully written in JS/TypeScript and depends on the `npm` package manager. Hence `npm` is a must to run UI.

### start-up

run:

```
cd ./scribe_ui
```

then:

```
npm install
```

to install all dependent packages. after that you can start UI with the:

```
npm run dev
```
