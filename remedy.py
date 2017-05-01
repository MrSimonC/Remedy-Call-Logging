import sys
import re
import os
import configparser
import base64
from PyQt4.QtGui import QApplication, QMainWindow, QFileDialog, QLineEdit, QPlainTextEdit, QMessageBox
from ui_mainwindow import Ui_MainWindow
from ui_settings import Ui_RemedySettings
from remedy_ie import RemedyIE
from custom_modules.xls import XlsTools
from sdplus_api_rest_nbt import ApiNbt
__version__ = '1.53'
# Written in start of Jan 2016, finished in the start of Feb 2016 due to IE8 being troublesome
# v0.4: Add note: 'Login Name: Logged to CSC.', allows 5th priority
# v0.4.1: moved remedy_ie
# v1.#: updated finding settings.cfg relative to this module/exe
# v1.4: removed switch_to_popup as doesn't work
# v1.5: added "AD Username" as using remedy_login.replace('.', ' ') doesn't apply for all users
# Add Refresh Button
# Add "Add myself as assignee" menu
# Add menu to optionally add Note
# Add button to pull in Subject from SDPlus

# MAKE MDS button!
# TODO: Add 2x attachments button - check max size?
# TODO: Why after logging does the update group/status disappear after a fraction of a second on status bar?


class Call:
    def __init__(self):
        """Defines a new remedy call object"""
        self.urgency = ''
        self.summary = ''
        self.name = ''
        self.users = ''
        self.sdplus_ref = ''
        self.mds_path = ''
        self.sdplus_tel = ''  # For SDPlus Call creation
        self.sdplus_description = ''  # For SDPlus Call creation

    def set_properties_from_mds(self, excel_mds):
        xl = XlsTools(excel_mds)
        try:
            self.urgency = str(int(xl.find('Local Severity (.)', 1)))
        except ValueError:
            self.urgency = ''
        self.summary = self._strip_if_ok(xl.find('Incident Description (.)', 1))
        self.name = self._strip_if_ok(xl.find("User's Name (.)", 1))
        try:
            self.users = self._strip_if_ok(str(int(xl.find('Number of Users Affected (.)', 1))))
        except ValueError:
            self.users = ''
        try:
            self.sdplus_ref = re.search(r'\d{6}', xl.find('Caller Reference', 1)).group(0)
        except AttributeError:  # optional local ref field omitted
            self.sdplus_ref = ''
        self.mds_path = os.path.abspath(excel_mds)
        self.sdplus_tel = self._strip_if_ok(xl.find("User's Phone Number (.)", 1))  # For SDPlus Call (and line below)
        self.sdplus_description = self._strip_if_ok(xl.find('Steps to recreate the Incident - How did I get here? (.)', 1))

    @staticmethod
    def _strip_if_ok(item):
        try:
            return item.strip()
        except AttributeError:
            return ''
        except ValueError:
            return ''


class Settings:
    def __init__(self):
        """Defines a object to hold all program settings"""
        # this_module's path
        if hasattr(sys, 'frozen'):
            self.this_module = os.path.dirname(sys.executable)
        else:
            self.this_module = os.path.dirname(os.path.realpath(__file__))
        self.config_file = os.path.join(self.this_module, 'settings.cfg')  # Hard Coded
        # Below set by set_properties_from_config_file()
        self.ad_username = ''
        self.remedy_login = ''
        self.remedy_password = ''
        self.remedy_url = ''
        self.details = ''
        self.service = ''
        self.sub_service = ''
        self.org = ''
        self.sdplus_api_technician_key = ''
        self.sdplus_api_url = ''

    def set_properties_from_config_file(self):
        config = configparser.ConfigParser()
        try:
            config.read(self.config_file)
        except FileNotFoundError:
            raise
        # AD
        self.ad_username = config.get('AD', 'ad_username')
        # Remedy Login
        self.remedy_login = config.get('REMEDY LOGIN', 'remedy_login')
        self.remedy_password = base64.b64decode(config.get('REMEDY LOGIN', 'remedy_password').encode()).decode()
        self.remedy_url = config.get('REMEDY LOGIN', 'remedy_url')
        # Remedy New Call
        self.details = config.get('REMEDY NEW CALL', 'details')
        self.service = config.get('REMEDY NEW CALL', 'service')
        self.sub_service = config.get('REMEDY NEW CALL', 'sub_service')
        self.org = config.get('REMEDY NEW CALL', 'org')
        # SDPlus API
        self.sdplus_api_technician_key = config.get('SDPLUS API', 'sdplus_api_technician_key')
        self.sdplus_api_url = config.get('SDPLUS API', 'sdplus_api_url')

    def write_properties_to_config_file(self):
        config = configparser.ConfigParser()
        config['AD'] = {
            'ad_username': self.ad_username,
        }
        config['REMEDY LOGIN'] = {
            'remedy_login': self.remedy_login,
            'remedy_password': base64.b64encode(self.remedy_password.encode()).decode(),
            'remedy_url': self.remedy_url
        }
        config['REMEDY NEW CALL'] = {
            'details': self.details,
            'service': self.service,
            'sub_service': self.sub_service,
            'org': self.org
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
        # Main Window
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.statusbar.showMessage('CSC Remedy Logging System (Version: ' + __version__ + ')', 5000)
        self.setup_connections()
        # Objects
        self.remedy_call = Call()
        self.settings = Settings()
        self.load_settings_config_file()
        self.remedy_ie = RemedyIE(self.settings.remedy_url, self.settings.remedy_login, self.settings.remedy_password)
        self.sdplus_api = ApiNbt(self.settings.sdplus_api_technician_key, self.settings.sdplus_api_url)
        self.settings_screen = None  # Placeholder for settings screen
        # Constants
        self.sdplus_queue_third_party = 'Back Office Third Party/CSC'
        self.sdplus_status_hold_awaiting_third = 'Hold - Awaiting Third Party'

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
        self.ui.refresh.clicked.connect(self.refresh)
        self.ui.pullSubject.clicked.connect(self.pull_subject)
        # Text Boxes
        self.ui.summary.textChanged.connect(self.summary_changed)
        self.ui.sdplus.textChanged.connect(self.sdplus_changed)
        self.ui.urgency.cursorPositionChanged.connect(self.urgency_clicked)
        self.ui.urgency.textChanged.connect(self.urgency_changed)
        self.ui.endUserName.textChanged.connect(self.end_user_name_changed)
        self.ui.affectedUsers.textChanged.connect(self.affected_users_changed)
        # Menu
        # File:
        self.ui.actionSettings.triggered.connect(self.show_settings)
        self.ui.actionReset_Form.triggered.connect(self.reset_form)
        self.ui.actionQuit.triggered.connect(app.quit)
        # SDPlus:
        self.ui.actionUpdate_Group_Status_add_Note_Assign_myself.triggered.connect(self.update_group_status_note_assign_myself)
        self.ui.actionUpdate_Group_Status_add_Note.triggered.connect(self.update_group_status_add_note)
        self.ui.actionUpdate_Group_and_Status.triggered.connect(self.update_group_and_status)
        self.ui.actionAttach_MDS_to_SDPlus_Record.triggered.connect(self.attach_mds_to_sdplus)
        self.ui.actionAdd_Note.triggered.connect(self.add_note)
        self.ui.actionAssign_Myself.triggered.connect(self.assign_myself)
        self.ui.actionUpdate_Group.triggered.connect(self.update_group_in_sdplus)
        self.ui.actionUpdate_Requester.triggered.connect(self.update_requester_in_sdplus)
        self.ui.actionUpdate_Status.triggered.connect(self.update_status_in_sdplus)
        self.ui.actionUpdate_Subject.triggered.connect(self.update_subject_in_sdplus)
        self.ui.actionUpdate_Urgency.triggered.connect(self.update_urgency_in_sdplus)
        # Creation Menu:
        self.ui.actionCreate_SDPlus_Record.triggered.connect(self.create_sdplus)
        # Help:
        self.ui.actionAbout.triggered.connect(self.about_dialog)

    # Buttons
    def load_xls(self):
        self.ui.statusbar.showMessage('Loading MDS', 5000)
        file_path = os.path.abspath(QFileDialog().getOpenFileName(self, "Open MDS", '',"Xlsx (*.xls)"))
        if os.path.isfile(file_path):
            self._set_properties_and_ui_from_mds_file(file_path)

    def log_new_remedy_issue(self):
        self.ui.statusbar.showMessage('Logging...', 5000)
        self.remedy_ie.login()
        self.remedy_ie.new_request(
            self.remedy_call.urgency,
            self.remedy_call.summary,
            self.settings.details,
            self.settings.service,
            self.settings.sub_service,
            self.settings.org,
            self.settings.remedy_login,
            self.remedy_call.name,
            self.remedy_call.users,
            self.remedy_call.sdplus_ref,
            self.remedy_call.mds_path
        )
        self.ui.statusbar.showMessage('Logging process complete.', 10000)

    def refresh(self):
        if os.path.isfile(self.remedy_call.mds_path):
            self._set_properties_and_ui_from_mds_file(self.remedy_call.mds_path)
        else:
            self.ui.statusbar.showMessage('Path is incorrect. Please Open MDS again.')

    def pull_subject(self):
        if self.remedy_call.sdplus_ref:
            subject_result = self.sdplus_api.request_view(self.remedy_call.sdplus_ref)
            self.remedy_call.summary = subject_result['subject'][:128]
            self.ui.summary.setPlainText(subject_result['subject'][:128])

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
        if not re.search('^[1-5]{1}$', self.ui.urgency.text()):
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
        self.settings_screen = GuiSettings(self.settings)
        self.settings_screen.show()

    def reset_form(self):
        for child in self.findChildren(QLineEdit):
            child.clear()
        for child in self.findChildren(QPlainTextEdit):
            child.clear()
        self.ui.statusbar.showMessage('Form Reset.', 5000)

    def update_group_status_note_assign_myself(self):
        status_result = self._update_group_and_status()
        note_result = self._add_note()
        assign_result = self._assign_myself()
        if status_result['response_status'] == 'Success' \
                and note_result['response_status'] == 'Success' \
                and assign_result['response_status'] == 'Success':
            self._update_status_bar(True)
        else:
            self._update_status_bar(False)

    def update_group_status_add_note(self):
        status_result = self._update_group_and_status()
        note_result = self._add_note()
        if status_result['response_status'] == 'Success' and note_result['response_status'] == 'Success':
            self._update_status_bar(True)
        else:
            self._update_status_bar(False)

    def update_group_and_status(self):
        status_result = self._update_group_and_status()
        if status_result['response_status'] == 'Success':
            self._update_status_bar(True)
        else:
            self._update_status_bar(False)

    def attach_mds_to_sdplus(self):
        attachment_result = self.sdplus_api.request_add_attachment(self.remedy_call.sdplus_ref,
                                                                   self.remedy_call.mds_path)
        if attachment_result['response_status'] == 'Success':
            self._update_status_bar(True)
        else:
            self._update_status_bar(False)

    def add_note(self):
        note_status = self._add_note()
        if note_status['response_status'] == 'Success':
            self._update_status_bar(True)
        else:
            self._update_status_bar(False)

    def assign_myself(self):
        assign_status = self._assign_myself()
        if assign_status['response_status'] == 'Success':
            self._update_status_bar(True)
        else:
            self._update_status_bar(False)

    def update_group_in_sdplus(self):
        fields = {'group': self.sdplus_queue_third_party}
        group_result = self.sdplus_api.request_edit(self.remedy_call.sdplus_ref, fields)
        if group_result['response_status'] == 'Success':
            self._update_status_bar(True)
        else:
            self._update_status_bar(False)

    def update_requester_in_sdplus(self):
        fields = {'requester': self.remedy_call.name}
        requester_result = self.sdplus_api.request_edit(self.remedy_call.sdplus_ref, fields)
        if requester_result['response_status'] == 'Success':
            self._update_status_bar(True)
        else:
            self._update_status_bar(False)

    def update_status_in_sdplus(self):
        fields = {'status': self.sdplus_status_hold_awaiting_third}
        status_result = self.sdplus_api.request_edit(self.remedy_call.sdplus_ref, fields)
        if status_result['response_status'] == 'Success':
            self._update_status_bar(True)
        else:
            self._update_status_bar(False)

    def update_subject_in_sdplus(self):
        fields = {'subject': self.remedy_call.summary}
        subject_result = self.sdplus_api.request_edit(self.remedy_call.sdplus_ref, fields)
        if subject_result['response_status'] == 'Success':
            self._update_status_bar(True)
        else:
            self._update_status_bar(False)

    def update_urgency_in_sdplus(self):
        fields = {'impact': self.sdplus_api.get_impact(self.remedy_call.urgency),
                  'urgency': self.sdplus_api.get_urgency(self.remedy_call.urgency)}
        urgency_result = self.sdplus_api.request_edit(self.remedy_call.sdplus_ref, fields)
        if urgency_result['response_status'] == 'Success':
            self._update_status_bar(True)
        else:
            self._update_status_bar(False)

    def create_sdplus(self):
        fields = {
            'reqtemplate': 'Default Request',
            'requesttype': 'Service Request',
            'status': self.sdplus_status_hold_awaiting_third,
            'requester': self.remedy_call.name,
            'mode': '@Southmead Retained Estate',  # Site
            'best contact number': self.remedy_call.sdplus_tel,
            'Exact Location': '-',
            'group': self.sdplus_queue_third_party,
            'subject': self.remedy_call.summary,
            'description': self.remedy_call.sdplus_description + '\n\n(This call was auto-created by '
                                                                 'Back Office from the MDS)',
            'service': '.Lorenzo/Galaxy - IT Templates',    # Service Category
            'category': 'Clinical Applications Incident',  # Self Service Incident
            'subcategory': 'Lorenzo',
            'impact': self.sdplus_api.get_impact(self.remedy_call.urgency),
            'urgency': self.sdplus_api.get_urgency(self.remedy_call.urgency),
            'technician': self.settings.ad_username
        }
        call_result = self.sdplus_api.request_add(fields)
        if call_result['response_status'] == 'Success':
            self.remedy_call.sdplus_ref = call_result['workorderid']
            self.ui.sdplus.setText(self.remedy_call.sdplus_ref)
            attachment_result = self.sdplus_api.request_add_attachment(self.remedy_call.sdplus_ref,
                                                                       self.remedy_call.mds_path)
            if attachment_result['response_status'] == 'Success':
                self._update_status_bar(True)
            return
        self._update_status_bar(False)

    def about_dialog(self):
        QMessageBox.about(self, "About", "CSC Remedy Call Logging System Helper\nBy Simon Crouch February 2016\n"
                                         "Version: " + __version__)

    # Helper methods
    def _set_properties_and_ui_from_mds_file(self, file_path):
        self.remedy_call.set_properties_from_mds(file_path)
        self.ui.summary.setPlainText(self.remedy_call.summary[:128])
        self.ui.sdplus.setText(self.remedy_call.sdplus_ref)
        self.ui.urgency.setText(self.remedy_call.urgency)
        self.ui.endUserName.setText(self.remedy_call.name)
        self.ui.affectedUsers.setText(self.remedy_call.users)
        self.ui.filepath.setText(self.remedy_call.mds_path)
        self.ui.statusbar.showMessage('MDS Loaded.', 5000)

    def _update_group_and_status(self):
        fields = {'group': self.sdplus_queue_third_party,
                  'status': self.sdplus_status_hold_awaiting_third}
        return self.sdplus_api.request_edit(self.remedy_call.sdplus_ref, fields)

    def _add_note(self):
        note_text = self.settings.ad_username + ': Logged to CSC'
        return self.sdplus_api.note_add(self.remedy_call.sdplus_ref, False, note_text)

    def _update_status_bar(self, success: bool):
        if success:
            self.ui.statusbar.showMessage('Update Successful.', 5000)
        else:
            self.ui.statusbar.showMessage('Update FAILED.', 5000)

    def _assign_myself(self):
        return self.sdplus_api.request_assign_name(self.settings.ad_username, self.remedy_call.sdplus_ref)


class GuiSettings(QMainWindow):
    def __init__(self, settings):
        """Defines the settings screen GUI"""
        # Objects
        self.settings = settings  # important. Don't do Settings(), but use settings object passed in
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
            self.ui.ad_username.setText(self.settings.ad_username)
            self.ui.remedy_username.setText(self.settings.remedy_login)
            self.ui.remedy_password.setText(self.settings.remedy_password)
            self.ui.remedy_url.setText(self.settings.remedy_url)
            self.ui.remedy_new_call_details.setText(self.settings.details)
            self.ui.remedy_new_call_service.setText(self.settings.service)
            self.ui.remedy_new_call_sub_service.setText(self.settings.sub_service)
            self.ui.remedy_new_call_org.setText(self.settings.org)
            self.ui.sdplus_tech_key.setText(self.settings.sdplus_api_technician_key)
            self.ui.sdplus_base_url.setText(self.settings.sdplus_api_url)
        except FileNotFoundError:
            self.ui.statusbar.showMessage("Can't find config file at all.")
        except configparser.NoSectionError:
            self.ui.statusbar.showMessage("Problem with a section in config file.")

    def save(self):
        self.settings.ad_username = self.ui.ad_username.text()
        self.settings.remedy_login = self.ui.remedy_username.text()
        self.settings.remedy_password = self.ui.remedy_password.text()
        self.settings.remedy_url = self.ui.remedy_url.text()
        self.settings.details = self.ui.remedy_new_call_details.text()
        self.settings.service = self.ui.remedy_new_call_service.text()
        self.settings.sub_service = self.ui.remedy_new_call_sub_service.text()
        self.settings.org = self.ui.remedy_new_call_org.text()
        self.settings.sdplus_api_technician_key = self.ui.sdplus_tech_key.text()
        self.settings.sdplus_api_url = self.ui.sdplus_base_url.text()
        self.settings.write_properties_to_config_file()
        self.ui.statusbar.showMessage('Saved.', 5000)


app = QApplication(sys.argv)
MainWindow = GuiMainWindow()
MainWindow.show()
sys.exit(app.exec_())
