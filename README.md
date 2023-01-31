# SLAM Dataset SDK


Due to increase in dataset targeted for SLAM, major gap is created in usability of the datasets. Major Datasets have there unique structure of storing and retrieving the sensor inputs. This project deals with combining all the dataset parsing and creating a simple and generic dataset interface, to enable fast evaluations and implementation of new SLAM systems. Due to cumbursome setup requirements for each dataset use, most of the time is consumed for just understanding how the dataset is sturctured and ways to decode them to be used for actual experiments. This created a delay and hence many implementations just use datasets which are easy to setup for experiments.
Our efforts are to reduce the gap between dataset and its usablity out of the box.
Additionally, we support basic Odometry pipeline stub, where user is allowed to use there custom deskew, registration functions enabling quick evaluation, without doing any tedious setup.
## Install

We released a python-package supported on
![ubuntu](https://img.shields.io/badge/ubuntu-333333?style=flat&logo=ubuntu).


To get started, just run

```sh
pip install slam-dataset-sdk
```

If you also want to install all the *(optional)* dependencies, like Open3D for running the visualizer:

```sh
pip install "slam-dataset-sdk[all]"
```


## Install (developer mode)

If you plan to modify the code then you need to setup the dev dependencies, luckilly, the only real
requirements are a modern C++ compiler and the `pip` package manager, nothing else!, in Ubuntu-based
sytems this can be done with:

```sh
sudo apt install g++ python3-pip
```

After that you can clone the code and install the python api:
```sh
git clone https://github.com/pranayspeed/slam_dataset_sdk.git
cd slam_dataset_sdk
pip install --verbose .
```

## Install (expert mode)

If you want to have more controll over the build, you should then install `cmake`, ,`ninja`, `tbb`,
`Eigen`, and `pybind11` as extra dependencies in your system, the ubuntu-way of doing this is:

```sh
sudo apt install build-essential libeigen3-dev libtbb-dev pybind11-dev ninja-build
```

## Using Library

Check slam_dataset_sdk/eval/sdk_test.py
A sample application is developed for example usage of the library

## Authors

- Pranay Meshram

## Credits

* Major code for Lidar dataset pre-processing is used from 'https://github.com/PRBonn/kiss-icp' [KISS-ICP: In Defense of Point-to-Point ICP -- Simple, Accurate, and Robust Registration If Done the Right Way](https://arxiv.org/pdf/2209.15397.pdf).

