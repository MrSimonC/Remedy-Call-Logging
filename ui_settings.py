# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'K:\Coding\Python\nbt work\Remedy Call Logging\settings.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_RemedySettings(object):
    def setupUi(self, RemedySettings):
        RemedySettings.setObjectName(_fromUtf8("RemedySettings"))
        RemedySettings.resize(310, 490)
        self.centralwidget = QtGui.QWidget(RemedySettings)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.remedy_username = QtGui.QLineEdit(self.centralwidget)
        self.remedy_username.setGeometry(QtCore.QRect(120, 80, 181, 20))
        self.remedy_username.setObjectName(_fromUtf8("remedy_username"))
        self.label = QtGui.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 80, 101, 16))
        self.label.setObjectName(_fromUtf8("label"))
        self.remedy_password = QtGui.QLineEdit(self.centralwidget)
        self.remedy_password.setGeometry(QtCore.QRect(120, 110, 181, 20))
        self.remedy_password.setEchoMode(QtGui.QLineEdit.Password)
        self.remedy_password.setObjectName(_fromUtf8("remedy_password"))
        self.label_2 = QtGui.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(10, 110, 101, 16))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.save = QtGui.QPushButton(self.centralwidget)
        self.save.setGeometry(QtCore.QRect(120, 430, 75, 23))
        self.save.setObjectName(_fromUtf8("save"))
        self.sdplus_tech_key = QtGui.QLineEdit(self.centralwidget)
        self.sdplus_tech_key.setGeometry(QtCore.QRect(120, 370, 181, 20))
        self.sdplus_tech_key.setText(_fromUtf8(""))
        self.sdplus_tech_key.setObjectName(_fromUtf8("sdplus_tech_key"))
        self.label_3 = QtGui.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(10, 370, 101, 16))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.line = QtGui.QFrame(self.centralwidget)
        self.line.setGeometry(QtCore.QRect(10, 320, 291, 20))
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.label_4 = QtGui.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(10, 140, 101, 16))
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.remedy_url = QtGui.QLineEdit(self.centralwidget)
        self.remedy_url.setGeometry(QtCore.QRect(120, 140, 181, 20))
        self.remedy_url.setEchoMode(QtGui.QLineEdit.Normal)
        self.remedy_url.setObjectName(_fromUtf8("remedy_url"))
        self.label_5 = QtGui.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(10, 400, 111, 16))
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.sdplus_base_url = QtGui.QLineEdit(self.centralwidget)
        self.sdplus_base_url.setGeometry(QtCore.QRect(120, 400, 181, 20))
        self.sdplus_base_url.setText(_fromUtf8(""))
        self.sdplus_base_url.setObjectName(_fromUtf8("sdplus_base_url"))
        self.remedy_new_call_service = QtGui.QLineEdit(self.centralwidget)
        self.remedy_new_call_service.setGeometry(QtCore.QRect(120, 240, 181, 20))
        self.remedy_new_call_service.setText(_fromUtf8(""))
        self.remedy_new_call_service.setObjectName(_fromUtf8("remedy_new_call_service"))
        self.label_6 = QtGui.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(10, 210, 101, 16))
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.remedy_new_call_details = QtGui.QLineEdit(self.centralwidget)
        self.remedy_new_call_details.setGeometry(QtCore.QRect(120, 210, 181, 20))
        self.remedy_new_call_details.setText(_fromUtf8(""))
        self.remedy_new_call_details.setObjectName(_fromUtf8("remedy_new_call_details"))
        self.label_7 = QtGui.QLabel(self.centralwidget)
        self.label_7.setGeometry(QtCore.QRect(10, 240, 111, 16))
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.label_8 = QtGui.QLabel(self.centralwidget)
        self.label_8.setGeometry(QtCore.QRect(10, 300, 111, 16))
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.remedy_new_call_sub_service = QtGui.QLineEdit(self.centralwidget)
        self.remedy_new_call_sub_service.setGeometry(QtCore.QRect(120, 270, 181, 20))
        self.remedy_new_call_sub_service.setText(_fromUtf8(""))
        self.remedy_new_call_sub_service.setObjectName(_fromUtf8("remedy_new_call_sub_service"))
        self.label_9 = QtGui.QLabel(self.centralwidget)
        self.label_9.setGeometry(QtCore.QRect(10, 270, 101, 16))
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.remedy_new_call_org = QtGui.QLineEdit(self.centralwidget)
        self.remedy_new_call_org.setGeometry(QtCore.QRect(120, 300, 181, 20))
        self.remedy_new_call_org.setText(_fromUtf8(""))
        self.remedy_new_call_org.setObjectName(_fromUtf8("remedy_new_call_org"))
        self.label_10 = QtGui.QLabel(self.centralwidget)
        self.label_10.setGeometry(QtCore.QRect(10, 180, 131, 20))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_10.setFont(font)
        self.label_10.setObjectName(_fromUtf8("label_10"))
        self.label_11 = QtGui.QLabel(self.centralwidget)
        self.label_11.setGeometry(QtCore.QRect(10, 50, 131, 20))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_11.setFont(font)
        self.label_11.setObjectName(_fromUtf8("label_11"))
        self.label_12 = QtGui.QLabel(self.centralwidget)
        self.label_12.setGeometry(QtCore.QRect(10, 340, 131, 20))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_12.setFont(font)
        self.label_12.setObjectName(_fromUtf8("label_12"))
        self.label_13 = QtGui.QLabel(self.centralwidget)
        self.label_13.setGeometry(QtCore.QRect(10, 0, 131, 20))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_13.setFont(font)
        self.label_13.setObjectName(_fromUtf8("label_13"))
        self.ad_username = QtGui.QLineEdit(self.centralwidget)
        self.ad_username.setGeometry(QtCore.QRect(120, 20, 181, 20))
        self.ad_username.setText(_fromUtf8(""))
        self.ad_username.setObjectName(_fromUtf8("ad_username"))
        self.label_14 = QtGui.QLabel(self.centralwidget)
        self.label_14.setGeometry(QtCore.QRect(10, 20, 101, 16))
        self.label_14.setObjectName(_fromUtf8("label_14"))
        RemedySettings.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(RemedySettings)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 310, 18))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        RemedySettings.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(RemedySettings)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        RemedySettings.setStatusBar(self.statusbar)

        self.retranslateUi(RemedySettings)
        QtCore.QMetaObject.connectSlotsByName(RemedySettings)
        RemedySettings.setTabOrder(self.remedy_username, self.remedy_password)
        RemedySettings.setTabOrder(self.remedy_password, self.remedy_url)
        RemedySettings.setTabOrder(self.remedy_url, self.remedy_new_call_details)
        RemedySettings.setTabOrder(self.remedy_new_call_details, self.remedy_new_call_service)
        RemedySettings.setTabOrder(self.remedy_new_call_service, self.remedy_new_call_sub_service)
        RemedySettings.setTabOrder(self.remedy_new_call_sub_service, self.remedy_new_call_org)
        RemedySettings.setTabOrder(self.remedy_new_call_org, self.sdplus_tech_key)
        RemedySettings.setTabOrder(self.sdplus_tech_key, self.sdplus_base_url)
        RemedySettings.setTabOrder(self.sdplus_base_url, self.save)

    def retranslateUi(self, RemedySettings):
        RemedySettings.setWindowTitle(_translate("RemedySettings", "Settings", None))
        self.label.setText(_translate("RemedySettings", "Remedy Username:", None))
        self.label_2.setText(_translate("RemedySettings", "Remedy Password:", None))
        self.save.setText(_translate("RemedySettings", "&Save", None))
        self.save.setShortcut(_translate("RemedySettings", "Ctrl+S", None))
        self.label_3.setText(_translate("RemedySettings", "SDPlus Tech Key:", None))
        self.label_4.setText(_translate("RemedySettings", "Remedy URL:", None))
        self.label_5.setText(_translate("RemedySettings", "SDPlus Base URL:", None))
        self.label_6.setText(_translate("RemedySettings", "Details:", None))
        self.label_7.setText(_translate("RemedySettings", "Service:", None))
        self.label_8.setText(_translate("RemedySettings", "Org:", None))
        self.label_9.setText(_translate("RemedySettings", "Sub Service:", None))
        self.label_10.setText(_translate("RemedySettings", "Remedy New Call", None))
        self.label_11.setText(_translate("RemedySettings", "Remedy Login", None))
        self.label_12.setText(_translate("RemedySettings", "SDPlus API", None))
        self.label_13.setText(_translate("RemedySettings", "AD (Windows) Login", None))
        self.label_14.setText(_translate("RemedySettings", "AD Username:", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    RemedySettings = QtGui.QMainWindow()
    ui = Ui_RemedySettings()
    ui.setupUi(RemedySettings)
    RemedySettings.show()
    sys.exit(app.exec_())

