
## PyQt5-tools

### Tool Installation

The PyQt5 package was installed to aid the development experience of QT5 GUIs.

**Note:** By default, this package would normally be installed in the (C:) drive, which
is outside the Python virtual environment corresponding to the rest of the project.

To install this package, the following command was used in the PyCharm (venv) terminal:

*pip install pyqt5-tools --target "$(pwd)/pyqt5-tools"*

This stores all the files related to PyQt5 locally in this repo (under the "pyqt5-tools" directory).

### Tool Usage

#### Starting the Designer.exe Application

The Designer.exe application was used to generate the initial GUI Qt5 objects (which were later
modified inside the respective scripts).

To start using this tool, navigate to the local "pyqt5-tools" folder in this repository, 
and run the following executable:

qt5_applications -> Qt -> bin -> designer.exe

**Note:** The (.ui) files produced in Designer.exe are different from the end products in the application.
This is because some modifications to the GUI were done outside of Designer.exe.

#### Producing Python code from (.ui) files

The PyQT5 designer tool will produce a (.ui) file of a single GUI "scene". This represents
the basic graphical layout of the UI, the remaining functionality must still be added using Python.

To produce usable Python code from the (.ui) file, run the following commands in the
PyCharm (venv) terminal [from the project base directory]:

pyuic5 -x pyqt5-tools/qt5_applications/Qt/bin/[ui_filename].ui -o [python_filename].py


