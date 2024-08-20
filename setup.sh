cp ./env_samples/env.txt ./.env
cp ./env_samples/pgpass.txt .

docker compose build
docker compose up -d