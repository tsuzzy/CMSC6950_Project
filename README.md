# CMSC6950_Project
Course Project for CMSC6950 Spring 2021

Ruixin Song


## Software setup

### Install conda
Though the latest Python version is already 3.9.x when writing this document, conda with Python-3.8.x environment is more recommanded in terms of to be compatible with the Visualization Tool Kit (VTK), which will be introduced and fixed later.

### Install Capytaine
After setting up conda, install the Capytaine module by:
```
conda install -c conda-forge capytaine
```
### Dependencies
Then, according to the Capytaine [document](https://ancell.in/capytaine/latest/user_manual/installation.html), you can install the dependencies that were not included in the capytaine module by:
```
conda install matplotlib
conda install vtk
```
However, the VTK part is not working on my machine, with an error like "vtk is incompatible with your python environment", since the VTK version accessed by conda can only support to Python 3.7.x. From the developers, the latest VTK wheel has been published supports Python-3.8, which can be reached by PyPl:
```
pip install vtk
```
If all work fine, the environment is set up!

## About the repository
Folder `examples`: I played around with some instances in the capytaine [documentation](https://ancell.in/capytaine/latest/user_manual/cookbook.html) and backup the code and results here. 