
## PyQT5-tools

### Tool Installation

This package was installed to aid the development experience of QT5 GUIs.

**Note:** By default, this package would normally be installed in the (C:) drive, which
is outside the Python virtual environment corresponding to the rest of the project.

To install this package, the following command was used in the PyCharm (venv) terminal:

*pip install pyqt5-tools --target "$(pwd)/pyqt5-tools"*

### Tool Usage

#### Starting the Designer.exe Application

To start using this tool, navigate to the local "pyqt5-tools" folder in this repository, 
and run the following executable:

qt5_applications -> Qt -> bin -> designer.exe

#### Producing Python code from (.ui) files

The PyQT5 designer tool will produce a (.ui) file of a single GUI "scene". This represents
the basic graphical layout of the UI, all the functionality must still be added using Python.

To produce usable Python code from the (.ui) file, run the following commands in the
PyCharm (venv) terminal:

pyuic5 -x pyqt5-tools/qt5_applications/Qt/bin/[ui_filename].ui -o [python_filename].py
