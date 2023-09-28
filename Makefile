drone:
	docker build -t sred21/drone:latest -f ./src/drone/Dockerfile ./src/drone

dc:
	docker build -t sred21/drone-controller:latest -f ./src/drone_controller/Dockerfile ./src/drone_controller

ac:
	docker build -t sred21/auto-controller:latest -f ./src/autonomous_controller/Dockerfile ./src/autonomous_controller

inf:
	docker build -t sred21/edge-server:latest -f ./src/inference_server/Dockerfile ./src/inference_server

push-drone:
	docker push sred21/drone:latest

push-dc:
	docker push sred21/drone-controller:latest

push-ac:
	docker push sred21/auto-controller:latest

push-inf:
	docker push sred21/edge-server:latest
