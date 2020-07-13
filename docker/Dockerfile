# Derived from official mysql image (our base image)
FROM mysql/mysql-server:latest

ENV MYSQL_DATABASE insights

# All scripts in docker-entrypoint-initdb.d/ are automatically
# executed during container startup
COPY ./sql-scripts/ /docker-entrypoint-initdb.d/
