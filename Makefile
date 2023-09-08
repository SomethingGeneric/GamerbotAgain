base:
	cd gamerthebase && docker build -t gamerthebase:latest .
build:
	docker compose build --no-cache
test: build
	docker compose up
stop:
	docker compose down
replace: stop build
	docker compose up -d