# -*- coding: utf-8 -*-
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.

from PyQt5 import QtCore, QtGui, QtWidgets
from gui_funcs import help_button_clicked, main_screen_ok_button_clicked, update_qt_text_str
from Received_MSG_GUI_Screen import Ui_results_window
from result_str_class import Result_String

class Ui_BLE_GATT_Client(object):

    def __init__(self):
        # We use a GET/SET approach for the result str due to how the Python namespaces between the GUI and func files are set up
        self.ble_server_reply_obj = Result_String()

    def open_results_window(self):
        print("The open_results_window func was called")
        ble_reply_str = self.ble_server_reply_obj.get_result_str()
        print("Updated String: " + ble_reply_str)
        self.window = QtWidgets.QDialog()
        self.ui = Ui_results_window()
        self.ui.setupUi(self.window)
        self.ui.reply_msg_label.setText(ble_reply_str)
        self.window.show()

    def setupUi(self, BLE_GATT_Client):

        BLE_GATT_Client.setObjectName("BLE_GATT_Client")
        BLE_GATT_Client.resize(400, 507)
        BLE_GATT_Client.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.default_buttonBox = QtWidgets.QDialogButtonBox(BLE_GATT_Client)
        self.default_buttonBox.setGeometry(QtCore.QRect(30, 460, 341, 32))
        self.default_buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.default_buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Help|
                                                  QtWidgets.QDialogButtonBox.Cancel|
                                                  QtWidgets.QDialogButtonBox.Ok)

        self.default_buttonBox.setObjectName("default_buttonBox")

        # The BLE Server GATT Read Characteristic UUID Label + Input Text Field
        self.BLE_Read_UUID = QtWidgets.QTextEdit(BLE_GATT_Client)
        self.BLE_Read_UUID.setGeometry(QtCore.QRect(40, 220, 321, 31))
        self.BLE_Read_UUID.setObjectName("BLE_Read_UUID")
        self.BLE_Server_Read_Label = QtWidgets.QLabel(BLE_GATT_Client)
        self.BLE_Server_Read_Label.setGeometry(QtCore.QRect(80, 180, 251, 21))
        self.BLE_Server_Read_Label.setStyleSheet("font: 9pt \"Arial\";")
        self.BLE_Server_Read_Label.setObjectName("BLE_Server_Read_Label")
        self.uuid_form_label_1 = QtWidgets.QLabel(BLE_GATT_Client)
        self.uuid_form_label_1.setGeometry(QtCore.QRect(40, 190, 341, 31))
        self.uuid_form_label_1.setObjectName("uuid_form_label_1")

        # The BLE Server GATT Write Characteristic UUID Label + Input Text Field
        self.BLE_Write_UUID = QtWidgets.QTextEdit(BLE_GATT_Client)
        self.BLE_Write_UUID.setGeometry(QtCore.QRect(40, 300, 321, 31))
        self.BLE_Write_UUID.setObjectName("BLE_Write_UUID")
        self.BLE_Server_Write_Label = QtWidgets.QLabel(BLE_GATT_Client)
        self.BLE_Server_Write_Label.setGeometry(QtCore.QRect(80, 260, 241, 21))
        self.BLE_Server_Write_Label.setStyleSheet("font: 9pt \"Arial\";")
        self.BLE_Server_Write_Label.setObjectName("BLE_Server_Write_Label")
        self.uui_form_label_2 = QtWidgets.QLabel(BLE_GATT_Client)
        self.uui_form_label_2.setGeometry(QtCore.QRect(40, 270, 341, 31))
        self.uui_form_label_2.setObjectName("uui_form_label_2")

        # The BLE Server Device Name Label + Input Text Field
        self.BLE_Server_Name_Label = QtWidgets.QLabel(BLE_GATT_Client)
        self.BLE_Server_Name_Label.setGeometry(QtCore.QRect(130, 20, 161, 21))
        self.BLE_Server_Name_Label.setStyleSheet("font: 10pt \"Arial\";")
        self.BLE_Server_Name_Label.setObjectName("BLE_Server_Name_Label")
        self.BLE_Device_Name = QtWidgets.QTextEdit(BLE_GATT_Client)
        self.BLE_Device_Name.setGeometry(QtCore.QRect(40, 50, 321, 31))
        self.BLE_Device_Name.setObjectName("BLE_Device_Name")

        # The BLE Server MAC Address Label + Input Text Field
        self.BLE_MAC_Address = QtWidgets.QTextEdit(BLE_GATT_Client)
        self.BLE_MAC_Address.setGeometry(QtCore.QRect(40, 120, 321, 31))
        self.BLE_MAC_Address.setObjectName("BLE_MAC_Address")
        self.BLE_Server_MAC_Label = QtWidgets.QLabel(BLE_GATT_Client)
        self.BLE_Server_MAC_Label.setGeometry(QtCore.QRect(100, 90, 201, 21))
        self.BLE_Server_MAC_Label.setStyleSheet("font: 10pt \"Arial\";")
        self.BLE_Server_MAC_Label.setObjectName("BLE_Server_MAC_Label")

        # The BLE Message Label + Input Text Field
        self.msg_string = QtWidgets.QTextEdit(BLE_GATT_Client)
        self.msg_string.setGeometry(QtCore.QRect(40, 370, 321, 51))
        self.msg_string.setObjectName("msg_string")
        self.BLE_Client_Msg_Label = QtWidgets.QLabel(BLE_GATT_Client)
        self.BLE_Client_Msg_Label.setGeometry(QtCore.QRect(40, 350, 241, 21))
        self.BLE_Client_Msg_Label.setStyleSheet("font: 9pt \"Arial\";")
        self.BLE_Client_Msg_Label.setObjectName("BLE_Client_Msg_Label")
        self.BLE_Client_Msg_Label.setWordWrap(True)

        # Help Button
        self.default_buttonBox.helpRequested.connect(help_button_clicked)

        # Calls the label functions and text
        self.retranslateUi(BLE_GATT_Client)

        # Note: When passing an argument to one of these functions, it starts expecting the function to be callable.
        # A function is callable when we pass an object as an input arg, or we pass no input arguments at all.
        # In our case, we need to invoke the non-callable function anonymously (using lambda) to avoid errors.
        self.default_buttonBox.accepted.connect(lambda: update_qt_text_str("ble_device_name", self.BLE_Device_Name.toPlainText()))
        self.default_buttonBox.accepted.connect(lambda: update_qt_text_str("ble_device_addr", self.BLE_MAC_Address.toPlainText()))
        self.default_buttonBox.accepted.connect(lambda: update_qt_text_str("ble_gatt_write_uuid", self.BLE_Write_UUID.toPlainText()))
        self.default_buttonBox.accepted.connect(lambda: update_qt_text_str("ble_gatt_read_uuid", self.BLE_Read_UUID.toPlainText()))
        self.default_buttonBox.accepted.connect(lambda: update_qt_text_str("ble_msg_str", self.msg_string.toPlainText()))
        self.default_buttonBox.accepted.connect(lambda: main_screen_ok_button_clicked(self.ble_server_reply_obj))  # Custom Function
        self.default_buttonBox.accepted.connect(lambda: self.open_results_window())  # Custom Function

        self.default_buttonBox.rejected.connect(BLE_GATT_Client.reject) # type: ignore

        QtCore.QMetaObject.connectSlotsByName(BLE_GATT_Client)

    def retranslateUi(self, BLE_GATT_Client):
        _translate = QtCore.QCoreApplication.translate
        BLE_GATT_Client.setWindowTitle(_translate("BLE_GATT_Client", "Dialog"))
        self.BLE_Server_Read_Label.setText(_translate("BLE_GATT_Client", "BLE Server Read GATT Characteristic UUID"))
        self.uuid_form_label_1.setText(_translate("BLE_GATT_Client", "Enter value in form: (xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx)"))
        self.BLE_Server_Write_Label.setText(_translate("BLE_GATT_Client", "BLE Server Write GATT Characteristic UUID"))
        self.uui_form_label_2.setText(_translate("BLE_GATT_Client", "Enter value in form: (xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx)"))
        self.BLE_Server_Name_Label.setText(_translate("BLE_GATT_Client", "BLE Server Device Name"))
        self.BLE_Server_MAC_Label.setText(_translate("BLE_GATT_Client", "BLE Server Device MAC Address"))
        self.BLE_Client_Msg_Label.setText(_translate("BLE_GATT_Client", "Message to send to BLE GATT Server"))
        #self.help_button.setText(_translate("BLE_GATT_Client", "Help"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    # Removes the annoying "?" button which is hard to access in the Python programming
    app.setAttribute(QtCore.Qt.ApplicationAttribute.AA_DisableWindowContextHelpButton)
    BLE_GATT_Client = QtWidgets.QDialog()
    ui = Ui_BLE_GATT_Client()
    ui.setupUi(BLE_GATT_Client)
    BLE_GATT_Client.show()
    sys.exit(app.exec_())
