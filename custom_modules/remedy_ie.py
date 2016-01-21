from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time


class RemedyIE:
    """
    Interacts with Remedy IE website
    """
    def __init__(self, url, username, password):
        self.url = url
        self.username = username
        self.password = password
        self.driver = None  # This is set in login not here else IE will open
        self.wait = None  # Set below, not here as self.drive above is None

    def login(self):
        # capabilities necessary for IE security settings being mixed
        capabilities = DesiredCapabilities.INTERNETEXPLORER
        capabilities['ignoreProtectedModeSettings'] = True
        # if frozen, webdriver.Ie() will look for IEDriverServer.exe in the current working directory
        self.driver = webdriver.Ie(capabilities=capabilities)
        self.wait = WebDriverWait(self.driver, 10)
        self.driver.maximize_window()
        self.driver.get(self.url)
        self.driver.find_element_by_id('username-id').send_keys(self.username)
        self.driver.find_element_by_id('pwd-id').send_keys(self.password)
        self.driver.execute_script('doLogin();')
        time.sleep(2)

    def new_request(self, urgency, summary, details, service, sub_service, org_down, login, name, users, ref, attachment):
        self.wait.until(EC.frame_to_be_available_and_switch_to_it((By.NAME, 'VF1575')))
        self.link_wait_click('Remedy Requester Console')
        self.link_wait_click('New Request')
        self.wait.until(EC.element_to_be_clickable((By.ID, 'arid240000009')))
        self.driver.find_element_by_id('arid240000009').click()  # Urgency
        for _ in range(0, int(urgency)):
            self.driver.find_element_by_id('arid240000009').send_keys(Keys.DOWN)
        self.driver.find_element_by_id('arid240000009').send_keys(Keys.RETURN)
        self.driver.find_element_by_id('arid260000008').click()  # Summary
        self.driver.find_element_by_id('arid260000008').send_keys(summary)
        self.driver.find_element_by_id('arid240000007').click()  # Details
        self.driver.find_element_by_id('arid240000007').send_keys(details)
        self.driver.find_element_by_id('arid300381700').click()  # Service
        time.sleep(1)
        self.driver.find_element_by_id('arid300381700').send_keys(service + Keys.RETURN)
        self.driver.find_element_by_id('arid767000049').click()  # Sub Service
        self.driver.find_element_by_id('arid767000049').send_keys(sub_service + Keys.RETURN)
        self.driver.find_element_by_id('arid766000022').click()  # Org - first click is to calculate Criticality
        self.driver.find_element_by_id('arid766000022').click()  # Org
        for _ in range(0, int(urgency)-1):
            self.driver.find_element_by_id('arid766000022').send_keys(Keys.DOWN)
        self.driver.find_element_by_id('arid766000022').send_keys(Keys.DOWN + Keys.RETURN)  # North Bristol
        self.driver.find_element_by_id('arid240000005').send_keys(login)
        self.driver.find_element_by_id('arid240000001').send_keys(name)
        self.driver.find_element_by_id('arid767000056').send_keys(users)
        self.driver.find_element_by_id('arid766000030').send_keys(ref)
        main_handle = self.driver.current_window_handle
        self.link_wait_click('Address Search')
        time.sleep(4)
        self.switch_to_new_window(main_handle)
        self.wait.until(EC.element_to_be_clickable((By.ID, 'arid536870915')))
        self.driver.find_element_by_id('arid536870915').send_keys('rvj01')
        self.driver.find_element_by_css_selector('.btn.btn3d.arfid536870909.ardbnbutSearch').click()  # Search
        time.sleep(1)
        self.driver.find_element_by_css_selector('.btn.btn3d.arfid536870908.ardbnbutSave').click()  # Save
        self.driver.switch_to.window(main_handle)
        self.driver.find_element_by_css_selector('.Add.btn.btn3d.TableBtn').click()  # Add
        self.switch_to_new_window(main_handle)
        self.driver.find_element_by_id('PopupAttInput').send_keys(attachment)
        self.driver.find_element_by_css_selector('.btn.btn3d.PopupBtn').click()  # OK
        self.driver.switch_to.window(main_handle)

        # self.link_wait_click('Save')  # Save button, main menu

    def switch_to_new_window(self, main_window_handle):
        for handle in self.driver.window_handles:
            if handle != main_window_handle:
                self.driver.switch_to.window(handle)

    def link_wait_click(self, link):
        self.wait.until(EC.element_to_be_clickable((By.LINK_TEXT, link)))
        self.driver.find_element_by_link_text(link).click()


# Example
if __name__ == '__main__':
    r = RemedyIE('https://rem-web.nme.ncrs.nhs.uk/arsys/shared/login.jsp', 'Simon.Crouch', 'Password1')
    r.login()
    r.new_request('3',
                  "Test: Messaging from Lorenzo allows update to patient's care record post discharge",
                  'See MDS',
                  'Lorenzo',
                  'Lorenzo',
                  'North Bristol NHS Trust',
                  'Simon.Crouch',
                  'Richard Pountney',
                  '6000',
                  '154133',
                  r'U:\auto_delete\REMEDY MDS_20160104_SDPlus154133.xls')
