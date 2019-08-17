dockerfile := "Dockerfile"
image_tag_name := "juniorxsound/exit-metadata:latest"

build:
	docker build -f ./$(dockerfile) -t $(image_tag_name) ./

build-clean:
	docker build --no-cache -f ./$(dockerfile) -t $(image_tag_name) ./

shell:
	docker run -w /data --rm -it -v `pwd`:/data -t $(image_tag_name) /bin/bash

jupyter:
	docker run -p 8888:8888 -w /data --rm -it -v `pwd`:/data -t $(image_tag_name) jupyter notebook --allow-root \

api:
	docker run -p 2912:2912 -w /data --rm -it -v `pwd`:/data -t $(image_tag_name) python ./gui/api.py

app:
	cd gui && yarn start