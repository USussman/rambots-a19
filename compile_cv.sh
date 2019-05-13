#!/bin/bash


DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
VENV=
PYVERSION=3.7.3

while getopts :hj:ln:s: option
do
    case "$option" in
    h)
         VENV=$OPTARG
         ;;
    v)
	 VERSION=$OPTARG
	 ;;
	 esac
done

sudo apt-get install screen

installPy(){
sudo apt-get update
sudo apt-get -y upgrade

wget https://www.python.org/ftp/python/$PYVERSION/Python-$PYVERSION.tgz
tar xf Python-$PYVERSION.tgz

cd Python-$PYVERSION/

./configure --enable-optimizations
make -j
make test
sudo make altinstall
}

installCV()
{
sudo apt-get -y purge wolfram-engine
sudo apt-get -y purge libreoffice*
sudo apt-get -y clean
sudo apt-get -y autoremove
sudo apt-get update && sudo apt-get -y upgrade
sudo apt-get install -y build-essential cmake pkg-config
sudo apt-get install -y libjpeg-dev libtiff5-dev libjasper-dev libpng12-dev
sudo apt-get install -y libavcodec-dev libavformat-dev libswscale-dev libv4l-dev
sudo apt-get install -y libxvidcore-dev libx264-dev
sudo apt-get install -y libgtk2.0-dev libgtk-3-dev
sudo apt-get install -y libatlas-base-dev gfortran
sudo apt-get install -y python2.7-dev python3-dev
cd ~
wget -O opencv.zip https://github.com/Itseez/opencv/archive/$VERSION.zip
unzip opencv.zip
wget -O opencv_contrib.zip https://github.com/Itseez/opencv_contrib/archive/$VERSION.zip
unzip opencv_contrib.zip

wget https://bootstrap.pypa.io/get-pip.py
sudo python get-pip.py
sudo python3 get-pip.py

if [ $VENV != ""]; then
    cd $DIR
    source $VENV/bin/activate
fi

pip install numpy --user

cd ~/opencv-$VERSION/
mkdir build
cd build

cmake -D CMAKE_BUILD_TYPE=RELEASE \
    -D CMAKE_INSTALL_PREFIX=/usr/local \
    -D INSTALL_PYTHON_EXAMPLES=ON \
    -D OPENCV_EXTRA_MODULES_PATH=~/opencv_contrib-$VERSION/modules \
    -D BUILD_EXAMPLES=ON ..
 
sudo sed '/CONF_SWAPSIZE=100/s/100/1024' /etc/dphys-swapfile

sudo /etc/init.d/dphys-swapfile stop
sudo /etc/init.d/dphys-swapfile start

make -j
sudo make install
sudo ldconfig

sudo sed '/CONF_SWAPSIZE=1024/s/1024/100' /etc/dphys-swapfile

deactivate
}

screen -S OpenCV -dm bash -c "installPy(); installCV(); exec sh"
