import sys
import re
import os
import configparser
import base64
from PyQt4.QtGui import QApplication, QMainWindow, QFileDialog, QLineEdit, QPlainTextEdit, QMessageBox
from ui_mainwindow import Ui_MainWindow
from ui_settings import Ui_RemedySettings
from custom_modules.remedy_ie import RemedyIE
from custom_modules.xls import XlsTools
from custom_modules.sdplus_api_rest import API
__version__ = '0.1'
# Written in start of Jan 2016


class Call:
    def __init__(self):
        """Defines a new remedy call object"""
        self.urgency = ''
        self.summary = ''
        self.name = ''
        self.users = ''
        self.sdplus_ref = ''
        self.mds_path = ''
        self.sdplus_tel = ''  # For SDPlus Call
        self.sdplus_description = ''  # For SDPlus Call

    def set_properties_from_mds(self, excel_mds):
        xl = XlsTools(excel_mds)
        try:
            self.urgency = str(int(xl.find('Local Severity (.)', 1)))
        except ValueError:
            self.urgency = ''
        self.summary = xl.find('Incident Description (.)', 1).strip()
        self.name = xl.find("User's Name (.)", 1).strip()
        self.users = str(int(xl.find('Number of Users Affected (.)', 1))).strip()
        self.sdplus_ref = re.search(r'\d{6}', xl.find('Caller Reference', 1)).group(0)
        self.mds_path = os.path.abspath(excel_mds)
        self.sdplus_tel = xl.find("User's Phone Number (.)", 1).strip()  # For SDPlus Call (and line below)
        self.sdplus_description = xl.find('Steps to recreate the Incident - How did I get here? (.)', 1).strip()


class Settings:
    def __init__(self):
        """Defines a object to hold all program settings"""
        # Hard Coded
        self.config_file = 'settings.cfg'
        # Overwritten by config file settings later
        self.remedy_login = ''
        self.remedy_password = ''
        self.remedy_url = 'https://rem-web.nme.ncrs.nhs.uk/arsys/shared/login.jsp'
        self.details = 'See MDS'
        self.service = 'l'
        self.sub_service = 'l'
        self.org_down = '1'
        self.sdplus_api_technician_key = '16EE6838-8160-4EFC-AEC1-0B35A59AF42C'
        self.sdplus_api_url = 'http://sdplus/sdpapi/request/'

    def set_properties_from_config_file(self):
        config = configparser.ConfigParser()
        if not os.path.exists(self.config_file):
            raise FileNotFoundError
        config.read(self.config_file)
        # Remedy Login
        self.remedy_login = config.get('REMEDY LOGIN', 'remedy_login')
        self.remedy_password = base64.b64decode(config.get('REMEDY LOGIN', 'remedy_password').encode()).decode()
        self.remedy_url = config.get('REMEDY LOGIN', 'remedy_url')
        # Remedy New Call
        self.details = config.get('REMEDY NEW CALL', 'details')
        self.service = config.get('REMEDY NEW CALL', 'service')
        self.sub_service = config.get('REMEDY NEW CALL', 'sub_service')
        self.org_down = config.get('REMEDY NEW CALL', 'org_down')
        # SDPlus API
        self.sdplus_api_technician_key = config.get('SDPLUS API', 'sdplus_api_technician_key')
        self.sdplus_api_url = config.get('SDPLUS API', 'sdplus_api_url')

    def write_properties_to_config_file(self):
        config = configparser.ConfigParser()
        config['REMEDY LOGIN'] = {
            'remedy_login': self.remedy_login,
            'remedy_password': base64.b64encode(self.remedy_password.encode()).decode(),
            'remedy_url': self.remedy_url
        }
        config['REMEDY NEW CALL'] = {
            'details': self.details,
            'service': self.service,
            'sub_service': self.sub_service,
            'org_down': self.org_down
        }
        config['SDPLUS API'] = {
            'sdplus_api_technician_key': self.sdplus_api_technician_key,
            'sdplus_api_url': self.sdplus_api_url
        }
        fileout = open(self.config_file, 'w', newline='')
        config.write(fileout)
        fileout.close()


class GuiMainWindow(QMainWindow):
    def __init__(self):
        """Defines the graphical elements and connectors to the main code"""
        # Objects
        self.remedy_call = Call()
        self.settings = Settings()
        self.remedy_ie = RemedyIE(self.settings.remedy_url, self.settings.remedy_login, self.settings.remedy_password)
        self.sdplus_api = API(self.settings.sdplus_api_technician_key, self.settings.sdplus_api_url)
        self.settings_screen = None  # Placeholder for settings screen
        # Main Window
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.statusbar.showMessage('CSC Remedy Logging System (Version: ' + __version__ + ')', 3000)
        self.load_settings_config_file()
        self.setup_connections()

    # Init Extended
    def load_settings_config_file(self):
        try:
            self.settings.set_properties_from_config_file()
        except FileNotFoundError:
            self.ui.statusbar.showMessage("Can't find config file at all.")
        except configparser.NoSectionError:
            self.ui.statusbar.showMessage("Problem with a section in config file.")

    def setup_connections(self):
        # Buttons
        self.ui.openMds.clicked.connect(self.load_xls)
        self.ui.logIssue.clicked.connect(self.log_new_remedy_issue)
        # Text Boxes
        self.ui.summary.textChanged.connect(self.summary_changed)
        self.ui.sdplus.textChanged.connect(self.sdplus_changed)
        self.ui.urgency.cursorPositionChanged.connect(self.urgency_clicked)
        self.ui.urgency.textChanged.connect(self.urgency_changed)
        self.ui.endUserName.textChanged.connect(self.end_user_name_changed)
        self.ui.affectedUsers.textChanged.connect(self.affected_users_changed)
        # Menu
        self.ui.actionSettings.triggered.connect(self.show_settings)
        self.ui.actionReset_Form.triggered.connect(self.reset_form)
        self.ui.actionQuit.triggered.connect(app.quit)
        self.ui.actionCreate_SDPlus_Record.triggered.connect(self.create_sdplus)
        self.ui.actionAttach_MDS_to_SDPlus_Record.triggered.connect(self.attach_mds_to_sdplus)
        self.ui.actionUpdate_Group.triggered.connect(self.update_group_in_sdplus)
        self.ui.actionUpdate_Requester.triggered.connect(self.update_requester_in_sdplus)
        self.ui.actionUpdate_Status.triggered.connect(self.update_status_in_sdplus)
        self.ui.actionUpdate_Subject.triggered.connect(self.update_subject_in_sdplus)
        self.ui.actionUpdate_Urgency.triggered.connect(self.update_urgency_in_sdplus)
        self.ui.actionAbout.triggered.connect(self.about_dialog)

    # Buttons
    def load_xls(self):
        self.ui.statusbar.showMessage('Loading MDS', 3000)
        file_path = os.path.abspath(QFileDialog().getOpenFileName(self, "Open MDS", '',"Xlsx (*.xls)"))
        if os.path.isfile(file_path):
            self.remedy_call.set_properties_from_mds(file_path)
            self.ui.summary.setPlainText(self.remedy_call.summary[:128])
            self.ui.sdplus.setText(self.remedy_call.sdplus_ref)
            self.ui.urgency.setText(self.remedy_call.urgency)
            self.ui.endUserName.setText(self.remedy_call.name)
            self.ui.affectedUsers.setText(self.remedy_call.users)
            self.ui.filepath.setText(self.remedy_call.mds_path)
            self.ui.statusbar.showMessage('MDS Loaded.', 2000)

    def log_new_remedy_issue(self):
        self.ui.statusbar.showMessage('Logging...', 3000)
        self.remedy_ie.login()
        self.remedy_ie.new_request(
            self.remedy_call.urgency,
            self.remedy_call.summary,
            self.settings.details,
            self.settings.service,
            self.settings.sub_service,
            self.settings.org_down,
            self.settings.remedy_login,
            self.remedy_call.name,
            self.remedy_call.users,
            self.remedy_call.sdplus_ref,
            self.remedy_call.mds_path
        )
        self.ui.statusbar.showMessage('Logging process complete.', 10000)

    # Text Boxes
    def summary_changed(self):
        if len(self.ui.summary.toPlainText()) > 128:
            self.ui.summary.textCursor().deletePreviousChar()
        self.remedy_call.summary = self.ui.summary.toPlainText()

    def sdplus_changed(self):
        self.remedy_call.sdplus_ref = self.ui.sdplus.text()

    def urgency_clicked(self):
        self.ui.urgency.selectAll()

    def urgency_changed(self):
        if not re.search('^[1-4]{1}$', self.ui.urgency.text()):
            self.ui.urgency.setText('')
        self.remedy_call.urgency = self.ui.urgency.text()

    def end_user_name_changed(self):
        self.remedy_call.name = self.ui.endUserName.text()

    def affected_users_changed(self):
        self.remedy_call.users = self.ui.affectedUsers.text()

    # Menu
    def show_settings(self):
        # Code works, but isn't needed:
        # self.settings_screen = QMainWindow()
        # self.settings_screen.ui = Ui_RemedySettings()
        # self.settings_screen.ui.setupUi(self.settings_screen)
        # self.settings_screen.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        # self.settings_screen.show()
        self.settings_screen = GuiSettings()
        self.settings_screen.show()

    def reset_form(self):
        for child in self.findChildren(QLineEdit):
            child.clear()
        for child in self.findChildren(QPlainTextEdit):
            child.clear()
        self.ui.statusbar.showMessage('Form Reset.', 2000)

    def create_sdplus(self):
        xml = self.sdplus_api.create_xml({
            'reqtemplate': 'Default Request',
            'requesttype': 'Service Request',
            'status': 'Hold - Awaiting Third Party',
            'requester': self.remedy_call.name,
            'mode': '@Southmead Retained Estate',  # Site
            'best contact number': self.remedy_call.sdplus_tel,
            'Exact Location': '-',
            'group': 'Back Office Third Party/CSC',
            'subject': self.remedy_call.summary,
            'description': self.remedy_call.sdplus_description + '\n\n(This call was auto-created by '
                                                                 'Back Office from the MDS)',
            'service': '.Lorenzo/Galaxy - IT Templates',    # Service Category
            'category': 'Clinical Applications Incident',  # Self Service Incident
            'subcategory': 'Lorenzo',
            'impact': self.get_impact(self.remedy_call.urgency),
            'urgency': self.get_urgency(self.remedy_call.urgency)
        })
        result = self.sdplus_api.send('', 'ADD_REQUEST', xml)
        if result['response_status'] == 'Success':
            self.remedy_call.sdplus_ref = result['workorderid']
            self.ui.sdplus.setText(self.remedy_call.sdplus_ref)
            self.ui.statusbar.showMessage('SDPlus call ' + self.remedy_call.sdplus_ref + ' created successfully.')
        else:
            self.ui.statusbar.showMessage('SDPlus call failed to be created')

    def attach_mds_to_sdplus(self):
        result = self.sdplus_api.send(self.remedy_call.sdplus_ref + '/attachment',
                                      'ADD_ATTACHMENT',
                                      attachment=self.remedy_call.mds_path)
        self.check_sdplus_api_response(result, 'Attachment added successfully',
                                       'Attachment failed to be added.')

    def update_group_in_sdplus(self):
        xml = self.sdplus_api.create_xml({'group': 'Back Office Third Party/CSC'})
        result = self.sdplus_api.send(self.remedy_call.sdplus_ref, 'EDIT_REQUEST', xml)
        self.check_sdplus_api_response(result, 'SDPlus group updated successfully',
                                       'SDPlus group failed to be updated.')

    def update_requester_in_sdplus(self):
        xml = self.sdplus_api.create_xml({'requester': self.remedy_call.name})
        result = self.sdplus_api.send(self.remedy_call.sdplus_ref, 'EDIT_REQUEST', xml)
        self.check_sdplus_api_response(result, 'SDPlus requester updated successfully',
                                       'SDPlus requester failed to be updated.')

    def update_status_in_sdplus(self):
        xml = self.sdplus_api.create_xml({'status': 'Hold - Awaiting Third Party'})
        result = self.sdplus_api.send(self.remedy_call.sdplus_ref, 'EDIT_REQUEST', xml)
        self.check_sdplus_api_response(result, 'SDPlus status updated successfully',
                                       'SDPlus status failed to be updated.')

    def update_subject_in_sdplus(self):
        xml = self.sdplus_api.create_xml({'subject': self.remedy_call.summary})
        result = self.sdplus_api.send(self.remedy_call.sdplus_ref, 'EDIT_REQUEST', xml)
        self.check_sdplus_api_response(result, 'SDPlus subject updated successfully',
                                       'SDPlus subject failed to be updated.')

    def update_urgency_in_sdplus(self):
        xml = self.sdplus_api.create_xml({'impact': self.get_impact(self.remedy_call.urgency),
                                          'urgency': self.get_urgency(self.remedy_call.urgency)})
        result = self.sdplus_api.send(self.remedy_call.sdplus_ref, 'EDIT_REQUEST', xml)
        self.check_sdplus_api_response(result, 'SDPlus urgency updated successfully',
                                       'SDPlus urgency failed to be updated.')

    def about_dialog(self):
        QMessageBox.about(self, "About", "CSC Remedy Call Logging System Helper\nBy Simon Crouch January 2016\n"
                                         "Version: " + __version__)

    # Helper methods
    def check_sdplus_api_response(self, api_response, status_bar_ok, status_bar_fail):
        if api_response['response_status'] == 'Success':
            self.ui.statusbar.showMessage(status_bar_ok)
        else:
            self.ui.statusbar.showMessage(status_bar_fail)

    @staticmethod
    def get_impact(digit):
        if digit == '1':
            return '1 Impacts Organisation'
        elif digit == '2':
            return '2 Impacts Site or Multiple Departments'
        elif digit == '3':
            return '3 Impacts Department'
        elif digit == '4':
            return '4 Impacts End User'
        else:
            return ''

    @staticmethod
    def get_urgency(digit):
        if digit == '1':
            return '1 Business Operations Severely Affected - Requires immediate response'
        elif digit == '2':
            return '2 Business Operations Significantly Affected - Requires response within 4 hours of created time'
        elif digit == '3':
            return '3 Business Operations Slightly Affected - Requires response within 8 hours of created time'
        elif digit == '4':
            return '4 Business Operations Not Affected - Requires response within 16 hours of created time'
        else:
            return ''


class GuiSettings(QMainWindow):
    def __init__(self):
        """Defines the settings screen GUI"""
        # Objects
        self.settings = Settings()
        # Gui
        QMainWindow.__init__(self)
        self.ui = Ui_RemedySettings()
        self.ui.setupUi(self)
        # Connectors
        self.ui.save.clicked.connect(self.save)
        # Setup
        self.load_gui_from_config()

    def load_gui_from_config(self):
        try:
            self.settings.set_properties_from_config_file()
            self.ui.remedy_username.setText(self.settings.remedy_login)
            self.ui.remedy_password.setText(self.settings.remedy_password)
            self.ui.remedy_url.setText(self.settings.remedy_url)
            self.ui.remedy_new_call_details.setText(self.settings.details)
            self.ui.remedy_new_call_service.setText(self.settings.service)
            self.ui.remedy_new_call_sub_service.setText(self.settings.sub_service)
            self.ui.remedy_new_call_org_down.setText(self.settings.org_down)
            self.ui.sdplus_tech_key.setText(self.settings.sdplus_api_technician_key)
            self.ui.sdplus_base_url.setText(self.settings.sdplus_api_url)
        except FileNotFoundError:
            self.ui.statusbar.showMessage("Can't find config file at all.")
        except configparser.NoSectionError:
            self.ui.statusbar.showMessage("Problem with a section in config file.")

    def save(self):
        self.settings.remedy_login = self.ui.remedy_username.text()
        self.settings.remedy_password = self.ui.remedy_password.text()
        self.settings.remedy_url = self.ui.remedy_url.text()
        self.settings.details = self.ui.remedy_new_call_details.text()
        self.settings.service = self.ui.remedy_new_call_service.text()
        self.settings.sub_service = self.ui.remedy_new_call_sub_service.text()
        self.settings.org_down = self.ui.remedy_new_call_org_down.text()
        self.settings.sdplus_api_technician_key = self.ui.sdplus_tech_key.text()
        self.settings.sdplus_api_url = self.ui.sdplus_base_url.text()
        self.settings.write_properties_to_config_file()
        self.ui.statusbar.showMessage('Saved.', 3000)


app = QApplication(sys.argv)
MainWindow = GuiMainWindow()
MainWindow.show()
sys.exit(app.exec_())
