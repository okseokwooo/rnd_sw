import threading
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

def seat_select(self):
    def task():
        self.driver.switch_to.default_content()
        self.driver.switch_to.frame(self.driver.find_elements(By.TAG_NAME, "ifrmSeat"))
        self.driver.switch_to.frame("ifrmSeatDetail")
        self.wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, 'img[src="http://ticketimage.interpark.com/TMGSNAS/TMGS/G/1_90.gif"]')))
        seats = self.driver.find_elements_by_css_selector(
            'img[src="http://ticketimage.interpark.com/TMGSNAS/TMGS/G/1_90.gif"]')
        print(len(seats))
        if int(self.seat_entry.get()) > len(seats):
            seat_count = len(seats)
        else:
            seat_count = int(self.seat_entry.get())
        for i in range(0, seat_count):
            seats[i].click()
        print("좌석 선택 완료")
        self.driver.switch_to.default_content()
        self.driver.switch_to.frame(self.driver.find_elements(By.TAG_NAME, "ifrmSeat"))
        self.driver.find_element(By.XPATH, "//*[@id='NextStepImage']").click()

    newthread = threading.Thread(target=task)
    newthread.start()