import threading
from selenium.common.exceptions import *
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time

def payment(self):
    def bank():
        try:
            self.driver.switch_to.frame(self.wait.until(EC.presence_of_element_located((By.ID, "ifrmBookStep"))))
            self.wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="Payment_22004"]/td/input'))).click()
            self.wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="BankCode"]/option[7]'))).click()
            self.driver.switch_to.default_content()
            time.sleep(2)
            self.driver.find_element(By.XPATH, '//*[@id="SmallNextBtnImage"]').click()
            self.driver.switch_to.frame(self.wait.until(EC.presence_of_element_located((By.ID, "ifrmBookStep"))))
            self.wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="checkAll"]'))).click()
            self.driver.switch_to.default_content()

        except UnexpectedAlertPresentException as e:
            print(f"Unexpected Alert: {e}")
            alert = self.driver.switch_to.alert
            alert.accept()

    def kakao():
        try:
            self.driver.switch_to.frame(self.wait.until(EC.presence_of_element_located((By.ID, "ifrmBookStep"))))
            self.wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="Payment_22084"]/td/input'))).click()
            self.driver.switch_to.default_content()
            time.sleep(2)
            self.driver.find_element(By.XPATH, '//*[@id="SmallNextBtnImage"]').click()
            self.driver.switch_to.frame(self.wait.until(EC.presence_of_element_located((By.ID, "ifrmBookStep"))))
            self.wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="checkAll"]'))).click()
            self.driver.switch_to.default_content()

        except UnexpectedAlertPresentException as e:
            print(f"Unexpected Alert: {e}")
            alert = self.driver.switch_to.alert
            alert.accept()

    def task():
        try:
            self.driver.switch_to.default_content()
            self.driver.find_element(By.XPATH, '//*[@id="SmallNextBtnImage"]').click()
            self.driver.switch_to.frame(self.wait.until(EC.presence_of_element_located((By.ID, "ifrmBookStep"))))
            self.wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="YYMMDD"]'))).send_keys(
                self.birth_entry.get())
            self.driver.switch_to.default_content()
            time.sleep(2)  # 대기 시간 추가
            self.driver.find_element(By.XPATH, '//*[@id="SmallNextBtnImage"]').click()

            bank2 = self.bank_var.get()
            kakao2 = self.kakao_var.get()

            if bank2 == 1:
                bank()
            elif kakao2 == 1:
                kakao()

        except UnexpectedAlertPresentException as e:
            print(f"Unexpected Alert: {e}")
            alert = self.driver.switch_to.alert
            alert.accept()

    newthread = threading.Thread(target=task)
    newthread.start()