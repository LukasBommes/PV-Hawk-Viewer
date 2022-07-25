import sys
from os.path import dirname, realpath
from setuptools import setup, find_packages

name = "src"

sys.path.insert(0, realpath(dirname(__file__))+"/"+name)

setup(
    name="PV-Hawk-Viewer",
    maintainer="Lukas Bommes",
    url='https://github.com/LukasBommes/PV-Hawk-Viewer',
    version="1.0.1", 
    packages=find_packages(),   
    package_dir={name: name},    
    include_package_data=True,
    license="MIT",
    description="Viewer for PV Hawk datasets.",
    install_requires=[
        "numpy>=1.19.1,<2",
        "pandas>=1.1.2,<2",
        "matplotlib>=3.5.0rc1,<4",
        "scikit-learn>=0.23.1,<2",
	"opencv-python>=4.2.0.34,<5",
	"networkx>=2.4,<3",
	"PySide6>=6.2.1,<6.2.4",
	"pyproj>=3.1.0,<4",
	"shapely>=1.7.1,<2"
    ],
    python_requires='>=3.8, <4',
    entry_points={"gui_scripts": ['viewer = src.__main__:main']},
    keywords=["PV Hawk", "Photovoltaic", "Defects", "Mapping", "PV Plant", "Drone", "Thermography"],
    classifiers=['Operating System :: OS Independent',
                'Programming Language :: Python :: 3',
                ],
    platforms=['ALL']
)
