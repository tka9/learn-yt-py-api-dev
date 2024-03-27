# learn-yt-py-api-dev
Learn Python API Development - Source Youtube 

# Postgres setup
docker run --name postgres -e POSTGRES_PASSWORD=adminadmin -p 5432:5432 -d postgres
docker run --name pgadmin4 -p 5050:80 -e PGADMIN_DEFAULT_EMAIL=user@domain.com -e PGADMIN_DEFAULT_PASSWORD=adminadmmin -d dpage/pgadmin4
docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' postgres

# CORS Test
fetch('http://localhost:8000/').then(res => res.json()).then(console.log)