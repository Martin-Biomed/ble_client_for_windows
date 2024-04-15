# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\pyqt5-tools\qt5_applications\Qt\bin\Received_MSG_GUI_Screen_Scrollbar.ui'
#
# Created by: PyQt5 UI code generator 5.15.10
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from field_format_funcs import ble_msg_result_str_dict, ble_msg_result_str
from GUI import API_Viewer_Dialog

# See the following for further guidance: https://www.pythonguis.com/tutorials/qscrollarea/

class Ui_results_dialog(object):

    # When the user presses the "Cancel" button, reset the value of the message string so its no longer accessible.
    def reset_reply_str_value(self):
        # Since this dict is global, the value of the result_str that can be accessed through the API is reset as well
        ble_msg_result_str_dict[ble_msg_result_str] = ''
        self.reply_msg_label.setText(ble_msg_result_str_dict[ble_msg_result_str])

    def open_api_viewer_dialog(self, Dialog):
        print("The open_api_viewer_dialog function was called.")
        self.api_viewer_dialog = API_Viewer_Dialog.MyDialog()
        self.ui = API_Viewer_Dialog.Ui_API_Viewer_Dialog()
        self.ui.setupUi(self.api_viewer_dialog)
        # The original Dialog box is replaced by the new Dialog Box
        Dialog.close()
        self.api_viewer_dialog.show()

    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        # We manually assign a fixed size for the main GUI Dialog Box
        Dialog.setFixedSize(400, 460)
        # We manually need to enable the "minimize" button for the dialog box
        Dialog.setWindowFlags(Dialog.windowFlags() | QtCore.Qt.WindowMinimizeButtonHint)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(300, 390, 81, 241))
        self.buttonBox.setOrientation(QtCore.Qt.Vertical)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel | QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")

        self.results_description_label = QtWidgets.QLabel(Dialog)
        self.results_description_label.setGeometry(QtCore.QRect(30, 20, 271, 16))
        self.results_description_label.setStyleSheet("font: 9pt \"Arial\";")
        self.results_description_label.setObjectName("results_description_label")

        self.publish_options_label = QtWidgets.QLabel(Dialog)
        self.publish_options_label.setGeometry(QtCore.QRect(30, 390, 251, 41))
        self.publish_options_label.setStyleSheet("font: 9pt \"Arial\";\n""font: 8pt \"MS Shell Dlg 2\";")
        self.publish_options_label.setWordWrap(True)
        self.publish_options_label.setObjectName("publish_options_label")

        self.scrollArea = QtWidgets.QScrollArea(Dialog)
        self.scrollArea.setGeometry(QtCore.QRect(40, 50, 321, 321))
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.reply_msg_scrollArea = QtWidgets.QWidget()
        self.reply_msg_scrollArea.setGeometry(QtCore.QRect(0, 0, 302, 1000))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.reply_msg_scrollArea.sizePolicy().hasHeightForWidth())
        self.reply_msg_scrollArea.setSizePolicy(sizePolicy)
        # To expand the scroll area (in case larger replies are expected), edit the QtCore.QSize
        self.reply_msg_scrollArea.setMinimumSize(QtCore.QSize(0, 1500))
        self.reply_msg_scrollArea.setObjectName("reply_msg_scrollArea")

        self.reply_msg_label = QtWidgets.QLabel(self.reply_msg_scrollArea)
        self.reply_msg_label.setGeometry(QtCore.QRect(0, 0, 321, 1000))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.reply_msg_label.sizePolicy().hasHeightForWidth())
        self.reply_msg_label.setSizePolicy(sizePolicy)
        # To expand the scroll area (in case larger replies are expected), edit the QtCore.QSize
        self.reply_msg_label.setMinimumSize(QtCore.QSize(0, 1500))
        self.reply_msg_label.setStyleSheet("font: 8pt \"Arial\";\n""background-color: rgb(255, 255, 255);")
        self.reply_msg_label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.reply_msg_label.setWordWrap(True)
        self.reply_msg_label.setObjectName("reply_msg_label")
        self.scrollArea.setWidget(self.reply_msg_scrollArea)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(lambda: self.open_api_viewer_dialog(Dialog))
        self.buttonBox.rejected.connect(lambda: self.reset_reply_str_value())
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.results_description_label.setText(_translate("Dialog", "Message received from selected BLE Server is:"))
        self.publish_options_label.setText(_translate("Dialog",
                                                      "Would you like to start the Application API server (http://localhost:5900)? "
                                                      " Press (Cancel) to reset the value of the message reply string."))
        self.reply_msg_label.setText(_translate("Dialog", "Received Message from BLE Server to be displayed here"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    #Dialog.setWindowModality(QtCore.Qt.ApplicationModal)
    ui = Ui_results_dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
