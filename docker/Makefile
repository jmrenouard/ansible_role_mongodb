NAME=mongodb-node
IMAGE=ubi8-mongodb-ansible:8.10
NETWORK=mongo-net

all: build network run

build:
	docker build -t $(IMAGE) .

network:
	docker network inspect $(NETWORK) >/dev/null 2>&1 || docker network create $(NETWORK)

run: network
	docker run -d --name $(NAME)-1 --network $(NETWORK) -p 2221:22 -p 27017:27017 $(IMAGE)
	docker run -d --name $(NAME)-2 --network $(NETWORK) -p 2222:22 -p 27018:27017 $(IMAGE)
	docker run -d --name $(NAME)-3 --network $(NETWORK) -p 2223:22 -p 27019:27017 $(IMAGE)

rebuild: clean ssh-clean all

ssh-clean:
	ssh-keygen -R "[localhost]:2221" > /dev/null 2>&1 || true
	ssh-keygen -R "[localhost]:2222" > /dev/null 2>&1 || true
	ssh-keygen -R "[localhost]:2223" > /dev/null 2>&1 || true

stop:
	docker stop $(NAME)-1 $(NAME)-2 $(NAME)-3 || true
	docker rm $(NAME)-1 $(NAME)-2 $(NAME)-3 || true

clean: stop
	docker network rm $(NETWORK) || true
	docker rmi $(IMAGE) || true

logs:
	docker logs -f $(NAME)-1

provision:
	./run_install.sh

deploy: all provision

# Build everything from scratch
scratch: clean all provision
