<h1 align="center">Image Extraction from EXIF Metadata</h1>
<p align="center">
<img src="https://github.com/juniorxsound/EXIF-Metadata-Image-Extraction/blob/master/samples/cover.png" alt="A depth-map extracted from iPhone Portait image" />
<br>
<b>Jupyter notebooks showing how to extract images from EXIF metadata 📝</b>
</p>

- [Getting Started](#getting-started)
- [Notebooks](#notebooks)
- [Enviorment](#enviorment)

## Getting Started 🚀
To quickly get started make sure you have [Docker installed](https://docs.docker.com/install/linux/docker-ce/ubuntu/) and do the following:
- Run `make build` to build the Docker container
- Run `make jupyter` to serve the Jupyter notebooks in `localhost:8888` 
- Open [localhost:8888](http://localhost:8888) in your browser and navigate to the notebook you want in the `notebooks/` folder
> Make sure you copy the full Jupyter token printed in the terminal

## Notebooks 📝
- [Lenovo Mirage 180 Stereo Camera - stereo exctraction](https://github.com/juniorxsound/EXIF-Metadata-Image-Extraction/blob/master/notebooks/Lenovo%20Mirage%20Camera.ipynb)
- [iPhone Portrait - depth extraction](https://github.com/juniorxsound/EXIF-Metadata-Image-Extraction/blob/master/notebooks/iPhone%20Portrait%20Depth.ipynb)

## Enviorment 🗻
This repo uses Docker to manage the dependencies. Here is a list of the available commands
- `make build` - build the Docker container
- `make build-clean` - build the Docker container and ignore cache
- `make shell` - `bash` into the Docker container
- `make jupyter` - run `jupyter` inside the container and map ports to `localhost:8888`
