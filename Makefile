DC = docker compose
EXEC = docker exec -it
LOGS = docker logs
ENV_FILE = --env-file .env
APP_CONTAINER = main-app
APP_FILE = docker-compose.yaml


.PHONY: app
app:
	${DC} -f ${APP_FILE} ${ENV_FILE} up --build -d


.PHONY: app-build
app-build:
	${DC} -f ${APP_FILE} ${ENV_FILE} build --no-cache


.PHONY: app-logs
app-logs:
	${LOGS} ${APP_CONTAINER} -f


.PHONY: app-down
app-down:
	${DC} -f ${APP_FILE} down

.PHONY: exec
exec:
	${EXEC} ${APP_CONTAINER}


