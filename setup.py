import sys
from os.path import dirname, realpath
from setuptools import setup, find_packages

name = "src"

sys.path.insert(0, realpath(dirname(__file__))+"/"+name)

setup(
    name="PV-Drone-Inspect-Viewer",
    maintainer="Lukas Bommes",
    url='https://github.com/LukasBommes/PV-Drone-Inspect-Viewer',
    version="1.0", 
    packages=find_packages(),   
    package_dir={name: name},    
    include_package_data=True,
    license="MIT",
    description="Viewer for PV Drone Inspect datasets.",
    install_requires=[
        "numpy>=1.19.1",
        "matplotlib>=3.5.0rc1",
        "geopandas>=0.9.0",
        "scikit-learn>=0.23.1",
        "opencv-python>=4.2.0.34",
        "networkx>=2.4",
        "PySide6>=6.2.1",
    ],
    python_requires='>=3.8, <4',
    entry_points={"gui_scripts": ['pvinspect = src.__main__:main']},
    keywords=["PV Drone Inspect", "Photovoltaic", "Defects", "Mapping", "PV Plant", "Drone", "Thermography"],
    classifiers=['Operating System :: OS Independent',
                'Programming Language :: Python :: 3',
                ],
    platforms=['ALL']
)