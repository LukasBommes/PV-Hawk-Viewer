# Howto build:
# >>> python setup.py build

import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning
build_exe_options = {
    "include_files": [
        ("src/resources/no_image.png", "src/resources/no_image.png"), 
        ("src/resources/app_icon.png", "src/resources/app_icon.png"),         
        ("src/resources/defect_schema.json", "src/resources/defect_schema.json"),
        ("src/index.html", "src/index.html"), 
        ("src/resources/web/style.css", "src/resources/web/style.css"), 
        ("src/resources/web/leaflet-1.7.1.js", "src/resources/web/leaflet-1.7.1.js"), 
        ("src/resources/web/leaflet-1.7.1.css", "src/resources/web/leaflet-1.7.1.css"), 
        ("src/resources/web/turf.js", "src/resources/web/turf.js"),
    ]
}

# base="Win32GUI" should be used only for Windows GUI app
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name = "PV-Map-Viewer",
    version = "1.0",
    description = "Viewer for PV-Mapper datasets.",
    options = {"build_exe": build_exe_options},
    executables = [Executable("main.py", base=base)]
)