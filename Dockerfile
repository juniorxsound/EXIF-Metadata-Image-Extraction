FROM tensorflow/tensorflow:latest-devel-py3
LABEL Author="Or Fleisher <contact@orfleisher.com>"
LABEL Title="EXIF Metadata extraction for stereo imagery"

# Add the user's bin to the path
ENV PATH "$PATH:/root/.local/bin"

# This fixes some locale issues with Pipenv inside the container
ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8

# Install all the other things we would need
RUN apt-get update && apt-get install -y \ 
    pkg-config \
    python-dev \ 
    libopencv-dev \ 
    libav-tools  \ 
    libjpeg-dev \ 
    libpng-dev \ 
    libtiff-dev \ 
    libjasper-dev \
    wget

# Install EXIF Tool (I know, kind of annoying it's not an apt-get install package)
RUN wget https://sno.phy.queensu.ca/~phil/exiftool/Image-ExifTool-11.38.tar.gz \ 
    && gzip -dc Image-ExifTool-11.38.tar.gz | tar -xf - \
    && cp -a Image-ExifTool-11.38/* /bin \
    && rm -rf Image-ExifTool-11.38.tar.gz \
    && rm -rf Image-ExifTool-11.38

WORKDIR /src
COPY requirements.txt .

# Install the python dependencies
RUN pip3 install --user -r requirements.txt