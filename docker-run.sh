# If this is an M1 mac, make sure we use docker QEMU amd64
if [[ $(uname -m) == 'arm64' ]]; then
  echo "Running on an M1 mac; setting to use amd64 images under QEMU"
  export DOCKER_DEFAULT_PLATFORM=linux/amd64
fi

docker-compose build
docker-compose run --rm web python manage.py migrate
docker-compose up
