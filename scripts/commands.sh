#!/bin/sh

# O shell irá encerrar a execução do script quando um comando falhar
set -e

psql.sh
migrate.sh
createuser.sh
pytest.sh
runserver.sh