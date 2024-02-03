import threading
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
def date_select(self):
    def task():
        while (True):
            try:
                self.driver.switch_to.frame(self.driver.find_element_by_id('ifrmBookStep'))
                if int(self.calender_entry.get()) == 0:
                    pass
                elif int(self.calender_entry.get()) >= 1:
                    for i in range(1, int(self.calender_entry.get()) + 1):
                        self.driver.find_element_by_xpath("/html/body/div/div[1]/div[1]/div/span[3]").click()
                try:
                    self.driver.find_element(By.XPATH, "//li[text()='" + self.date_entry.get() + "']").click()
                    break
                except NoSuchElementException:
                    self.link_go()
                    break
            except NoSuchElementException:
                self.link_go()
                break
        self.wait.until(EC.element_to_be_clickable(
            (By.CLASS_NAME, "timeTableItem" + [self.round_entry.get() - 1]))).click()
        self.driver.switch_to.default_content()
        self.driver.find_element_by_id('LargeNextBtnImage').click()

    newthread = threading.Thread(target=task)
    newthread.start()