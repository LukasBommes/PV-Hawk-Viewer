#import sys
from setuptools import setup, find_packages

# Dependencies are automatically detected, but it might need fine tuning
# build_exe_options = {
#     "include_files": [
#         ("src/resources/no_image.png", "src/resources/no_image.png"), 
#         ("src/resources/app_icon.png", "src/resources/app_icon.png"),  
#         ("src/resources/sun_icon.png", "src/resources/sun_icon.png"),    
#         ("src/resources/no_sun_icon.png", "src/resources/no_sun_icon.png"),  
#         ("src/resources/defect_schema.json", "src/resources/defect_schema.json"),
#         ("src/index.html", "src/index.html"), 
#         ("src/resources/web/style.css", "src/resources/web/style.css"), 
#         ("src/resources/web/leaflet-1.7.1.js", "src/resources/web/leaflet-1.7.1.js"), 
#         ("src/resources/web/leaflet-1.7.1.css", "src/resources/web/leaflet-1.7.1.css"), 
#         ("src/resources/web/turf.js", "src/resources/web/turf.js"),
#     ]
# }

# base="Win32GUI" should be used only for Windows GUI app

setup(
    name="Dataset Viewer for PV Drone Inspect",
    maintainer="Lukas Bommes",
    url='https://github.com/LukasBommes/PV-Drone-Inspect-Viewer',
    version="1.0",
    packages=find_packages(),
    package_dir={"src": "src"},
    include_package_data=True,
    license="MIT",
    description="Viewer for PV Drone Inspect datasets.",
    install_requires=[
        "PySide6>=6.2.2",
    ],
    python_requires='>=3.8, <4',
    entry_points={"gui_scripts": ['pvinspect = main.__main__:main']},
    #keywords=[],
    #classifiers=['Operating System :: OS Independent',
    #             'Programming Language :: Python :: 3',
    #             'Intended Audience :: Science/Research',
    #             ],
    platforms=['ALL']

    #options = {"build_exe": build_exe_options},
    #executables = [Executable("main.py", base=base)]
)