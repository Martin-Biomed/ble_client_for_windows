
from PyQt5 import QtCore, QtWidgets
import src.GUI.BLE_Client_Init_Dialog
import sys
import os
import logging

if __name__ == '__main__':

    # Configure Logging for the rest of the program
    default_log_dir = "C:\BLE_Client_Logs"
    default_log_filename = "C:\BLE_Client_Logs\BLE_GATT_Client.log"
    if os.path.exists(default_log_dir):
        if os.path.exists(default_log_filename):
            os.remove(default_log_filename)
    else:
        os.mkdir(default_log_dir)

    logging.basicConfig(filename=default_log_filename, filemode='w', level=logging.INFO)

    # execute only if run as the entry point into the program
    app = QtWidgets.QApplication(sys.argv)
    # Removes the annoying "?" button which is hard to access in the Python programming
    app.setAttribute(QtCore.Qt.ApplicationAttribute.AA_DisableWindowContextHelpButton)
    Dialog = QtWidgets.QDialog()
    ui = src.GUI.BLE_Client_Init_Dialog.Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())