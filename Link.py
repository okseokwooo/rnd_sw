import threading
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time

def link_go(self):
    def task():
        self.driver.get('http://poticket.interpark.com/Book/BookSession.asp?GroupCode=' + self.showcode_entry.get())

    try:
        popup_close_button = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="popup-prdGuide"]/div/div[3]/button'))
        )
        popup_close_button.click()
    except:
        pass

    newthread = threading.Thread(target=task)
    newthread.start()