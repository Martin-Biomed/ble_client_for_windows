
from PyQt5 import QtCore, QtWidgets
import src.GUI.BLE_Client_Init_Dialog

if __name__ == '__main__':
    # execute only if run as the entry point into the program
    import sys
    app = QtWidgets.QApplication(sys.argv)
    # Removes the annoying "?" button which is hard to access in the Python programming
    app.setAttribute(QtCore.Qt.ApplicationAttribute.AA_DisableWindowContextHelpButton)
    Dialog = QtWidgets.QDialog()
    ui = src.GUI.BLE_Client_Init_Dialog.Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())