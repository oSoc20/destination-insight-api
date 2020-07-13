## Build docker container:

docker build -t destination-insight .

## start container
docker run -d -p 3306:3306 --name destination-insight -e MYSQL_ROOT_PASSWORD=supersecret destination-insight

When running the scripts in the sql-scripts dir will automatically be executed!

## Stopping the container

	docker stop destination-insight

## Removing the container and rebuilding (when for example new scripts are added)

You can only remove stopped containers.


	docker rm destination-insight
	
	docker build -t destination-insight .

	(then run the container again, see step 2)