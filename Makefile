PLATFORM = linux/amd64

all:
	echo "Building image: drone"
	docker build --platform $(PLATFORM) -t sred21/drone:latest -f ./src/drone/Dockerfile ./src/drone
	
	echo "Building image: drone-controller"
	docker build --platform $(PLATFORM) -t sred21/drone-controller:latest -f ./src/drone_controller/Dockerfile ./src/drone_controller

	echo "Building image: auto-controller"
	docker build --platform $(PLATFORM) -t sred21/auto-controller:latest -f ./src/autonomous_controller/Dockerfile ./src/autonomous_controller

	echo "Building image: inference-server"
	docker build --platform $(PLATFORM) -t sred21/edge-server:latest -f ./src/inference_server/Dockerfile ./src/inference_server


drone:
	docker build --platform $(PLATFORM) -t sred21/drone:latest -f ./src/drone/Dockerfile ./src/drone

dc:
	docker build --platform $(PLATFORM) -t sred21/drone-controller:latest -f ./src/drone_controller/Dockerfile ./src/drone_controller

ac:
	docker build --platform $(PLATFORM) -t sred21/auto-controller:latest -f ./src/autonomous_controller/Dockerfile ./src/autonomous_controller

inf:
	docker build --platform $(PLATFORM) -t sred21/edge-server:latest -f ./src/inference_server/Dockerfile ./src/inference_server

push:
	echo "Pushing all images to the docker hub"
	docker push sred21/drone:latest
	docker push sred21/drone-controller:latest
	docker push sred21/auto-controller:latest	
	docker push sred21/edge-server:latest




push-drone:
	docker push sred21/drone:latest

push-dc:
	docker push sred21/drone-controller:latest

push-ac:
	docker push sred21/auto-controller:latest

push-inf:
	docker push sred21/edge-server:latest
