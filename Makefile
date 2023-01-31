docker-build:
	docker build -t music-library:1.0 .

docker-run:
	docker run -p 5000:5000 music-library:1.0
