docker-compose build
docker-compose run --rm web python manage.py migrate
docker-compose up
