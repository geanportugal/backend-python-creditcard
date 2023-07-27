#!/bin/sh
echo "🟡 Criando usuário"
echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('$SUPERUSER_USERNAME', '$SUPERUSER_EMAIL', '$SUPERUSER_PASSWORD')" | python manage.py shell
echo "🟢 usuário criado!!!!!"
pytest.sh
