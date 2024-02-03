import threading
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
def login(self):
    def task():
        try:
            iframe = self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "iframe")))
            self.driver.switch_to.frame(iframe)
            self.driver.find_element(By.CSS_SELECTOR, "#userId").send_keys(self.id_entry.get())
            self.driver.find_element(By.CSS_SELECTOR, "#userPwd").send_keys(self.pw_entry.get())
            self.driver.find_element(By.CSS_SELECTOR, "#btn_login").click()
        except NoSuchElementException:
            print("로그인 요소를 찾을 수 없음")
        finally:
            self.driver.switch_to.default_content()

    newthread = threading.Thread(target=task)
    newthread.start()