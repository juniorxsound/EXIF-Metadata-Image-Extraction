dockerfile := "Dockerfile"

build:
	docker build -f ./$(dockerfile) -t juniorxsound/exit-stereo-metadata:latest ./

build-clean:
	docker build --no-cache -f ./$(dockerfile) -t juniorxsound/exit-stereo-metadata:latest ./

shell:
	docker run -w /data --rm -it -v `pwd`:/data -t juniorxsound/exit-stereo-metadata:latest /bin/bash

jupyter:
	docker run -p 8888:8888 -w /data --rm -it -v `pwd`:/data -t juniorxsound/exit-stereo-metadata:latest jupyter notebook --ip 0.0.0.0 --allow-root \