<h1 align=center>🌟Проект Foodgram - Продуктовый помощник🌟</h1>

## 📄 **Описание**

Foodgram - вебсайт с рецептами, позволяет:

- Создавать, просматривать, редактировать и удалять рецепты блюд.
- Просматривать рецепты и добавлять, удалять их из списока избраных.
- Добавлять, и удалять из корзины свои и чужие рецепты, и скачавать список продуктов необходимый для их приготовления.
- Добавлять авторов в подписки и просматривать все рецепты автора на которого подписались.
  
<br>
<br>

## 🛠️ Инструкция по установке
___
### Установка на локальный компьютер.

Клонируйте репозиторий:

```
git clone git@github.com:vglazasmotri/foodgram-project-react.git
```

```
cd foodgram-project-react
```

Создайте файл .env и заполните его своими данными. Пример в файле .env.example:

```
# Переменные для базы данных:
POSTGRES_DB=foodgram
POSTGRES_USER=foodgram_user
POSTGRES_PASSWORD=foodgram_password
DB_NAME=foodgram
# для Django-проекта:
DB_HOST=db
DB_PORT=5432
SECRET_KEY=secret_key
ALLOWED_HOSTS="***.*.*.*,127.0.0.1,localhost,you_domen"
DEBUG=False
# для Docker:
BACKEND_PORT=8000
HTTP_PORT=80
DOCKER_USERNAME=dockerhub_username
APPLICATION_NAME=foodgram
```

Установить пакет Make:

Если у вас Windows.
- Установите chocolatey package manager
- Установите make:
```
choco install make
```
Если у вас Linux то make должна быть установлена по умолчанию. На всякий случай:
```
sudo apt install make
```

Создание Docker-образов и загрузка на ваш DockerHub с помощью Makefile:

```
cd frontend
make build push
```

```
cd ../backend
make build push
```

Запуск проекта на локальном компьютере:

```
cd ../infra
docker compose -f docker-compose.production.yml up
```

Соберите статику, скопируйте файлы и выполните команду migrate в Windows лучше через PowerShell:

```
docker compose -f docker-compose.production.yml exec backend python manage.py collectstatic
```

```
docker compose -f docker-compose.production.yml exec backend cp -r /app/collected_static/. /backend_static/
```
```
docker compose -f docker-compose.production.yml exec backend python manage.py makemigrations
```
```
docker compose -f docker-compose.production.yml exec backend python manage.py migrate
```

Проект доступер локально

```
http://localhost:8000/
```

___
### Деплой на сервер.

Подключитесь к удаленному серверу

```
ssh -i путь_до_файла_с_SSH_ключом/название_файла_с_SSH_ключом имя_пользователя@ip_адрес_сервера 
```

Создайте на сервере директорию foodgram через терминал:

```
mkdir foodgram
```

Установка docker compose на сервер:

```
sudo apt update
sudo apt install curl
curl -fSL https://get.docker.com -o get-docker.sh
sudo sh ./get-docker.sh
sudo apt-get install docker-compose-plugin
```

На сервере в директорию foodgram/ скопируйте файлы из локальной папки infra: docker-compose.production.yml, nginx.conf и .env:

```
scp -i path_to_SSH/SSH_name docker-compose.production.yml username@server_ip:/home/username/foodgram/docker-compose.production.yml
```
* ath_to_SSH — путь к файлу с SSH-ключом;
* SSH_name — имя файла с SSH-ключом (без расширения);
* username — ваше имя пользователя на сервере;
* server_ip — IP вашего сервера.

Или создайте аналогичные файлы с помощью редактора, например nano и скопруйте в них содержимое.

Запустите docker compose в режиме демона:

```
sudo docker compose -f docker-compose.production.yml up -d
```

Выполните миграции, соберите статические файлы бэкенда и скопируйте их в /backend_static/:

```
sudo docker compose -f docker-compose.production.yml exec backend python manage.py makemigrations
```

```
sudo docker compose -f docker-compose.production.yml exec backend python manage.py migrate
```

```
sudo docker compose -f docker-compose.production.yml exec backend python manage.py collectstatic
```

```
sudo docker compose -f docker-compose.production.yml exec backend cp -r /app/collected_static/. /backend_static/
```

Создайте суперпользователя
```
sudo docker compose -f docker-compose.production.yml exec backend python manage.py createsuperuser
```

Импортируйте и список ингредиентов в бд


```
sudo docker compose -f docker-compose.production.yml exec backend python manage.py ingredients_from_data ingredients.csv
```

На сервере в редакторе nano откройте конфиг Nginx:

```
sudo nano /etc/nginx/sites-enabled/default
```

Измените настройки location в секции server:

```
location / {
    proxy_set_header Host $http_host;
    proxy_pass http://127.0.0.1:8000;
}
```

Проверьте работоспособность конфига Nginx:

```
sudo nginx -t
```

Если ответ в терминале такой, значит, ошибок нет:
```
nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
nginx: configuration file /etc/nginx/nginx.conf test is successful
```

Перезапускаем Nginx

```
sudo service nginx reload
```

Готово!


<br>
<br>

## 🎞️ Примеры

[Дэмо проекта](http://foodgramm.ru/recipes)

## 🛠️ Применяемые технологии:
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) ![DjangoREST](https://img.shields.io/badge/DJANGO-REST-ff1709?style=for-the-badge&logo=django&logoColor=white&color=ff1709&labelColor=blue) ![JavaScript](https://img.shields.io/badge/javascript-%23323330.svg?style=for-the-badge&logo=javascript&logoColor=%23F7DF1E) ![React](https://img.shields.io/badge/react-%2320232a.svg?style=for-the-badge&logo=react&logoColor=%2361DAFB) ![Ubuntu](https://img.shields.io/badge/Ubuntu-E95420?style=for-the-badge&logo=ubuntu&logoColor=white) ![Gunicorn](https://img.shields.io/badge/gunicorn-%298729.svg?style=for-the-badge&logo=gunicorn&logoColor=white) ![Nginx](https://img.shields.io/badge/nginx-%23009639.svg?style=for-the-badge&logo=nginx&logoColor=white)
- Python 3.7
- Django 3.2
- Django Rest Framework 3.12.4


## 💪 Автор:

- Сергей Сыч Python-разработчик (https://github.com/vglazasmotri)
