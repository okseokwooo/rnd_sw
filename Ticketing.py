import threading
from tkinter import *
from selenium.common.exceptions import *
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
import time
class App(threading.Thread):
    def __init__(self):
        super().__init__()
        self.driver = webdriver.Chrome()
        self.wait = WebDriverWait(self.driver, 10)
        self.url = "https://ticket.interpark.com/Gate/TPLogin.asp"
        self.driver.get(self.url)

        # tkinter
        self.dp = Tk()
        self.dp.geometry("500x500")
        self.dp.title("인터파크 티케팅 프로그램")
        self.object_frame = Frame(self.dp)
        self.object_frame.pack()

        self.id_label = Label(self.object_frame, text="ID")
        self.id_label.grid(row=1, column=0)
        self.id_entry = Entry(self.object_frame, width=40)
        self.id_entry.grid(row=1, column=1)
        self.pw_label = Label(self.object_frame, text="PASSWORD")
        self.pw_label.grid(row=2, column=0)
        self.pw_entry = Entry(self.object_frame, show="*", width=40)
        self.pw_entry.grid(row=2, column=1)
        self.showcode_label = Label(self.object_frame, text="공연번호")
        self.showcode_label.grid(row=4, column=0)
        self.showcode_entry = Entry(self.object_frame, width=40)
        self.showcode_entry.grid(row=4, column=1)
        self.calender_ladel = Label(self.object_frame, text="달력")
        self.calender_ladel.grid(row=6, column=0)
        self.calender_entry = Entry(self.object_frame, width=40)
        self.calender_entry.grid(row=6, column=1)
        self.date_label = Label(self.object_frame, text="날짜")
        self.date_label.grid(row=7, column=0)
        self.date_entry = Entry(self.object_frame, width=40)
        self.date_entry.grid(row=7, column=1)
        self.round_label = Label(self.object_frame, text="회차")
        self.round_label.grid(row=8, column=0)
        self.round_entry = Entry(self.object_frame, width=40)
        self.round_entry.grid(row=8, column=1)
        self.seat_label = Label(self.object_frame, text="좌석 수")
        self.seat_label.grid(row=9, column=0)
        self.seat_entry = Entry(self.object_frame, width=40)
        self.seat_entry.grid(row=9, column=1)
        self.birth_label = Label(self.object_frame, text="생년월일")
        self.birth_label.grid(row=11, column=0)
        self.birth_entry = Entry(self.object_frame, width=40, show='*')
        self.birth_entry.grid(row=11, column=1)
        self.bank_var = IntVar(value=0)
        self.bank_check = Checkbutton(self.object_frame, text='무통장', variable=self.bank_var)
        self.bank_check.grid(row=12, column=0)
        self.kakao_var = IntVar(value=0)
        self.kakao_check = Checkbutton(self.object_frame, text='카카오', variable=self.kakao_var)
        self.kakao_check.grid(row=12, column=1)
        self.test2_button = Button(self.object_frame, text="실행", width=3, height=2, command=self.run_multiple_commands)
        self.test2_button.grid(row=12, column=2)
        self.dp.mainloop()

    # 로그인 하기
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

    # 직링 바로가기
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

    # 날짜 선택
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

    # 좌석 선택
    def seat_select(self):
        def task():
            self.driver.switch_to.default_content()
            self.driver.switch_to.frame(self.driver.find_elements(By.TAG_NAME,"ifrmSeat"))
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
            self.driver.switch_to.frame(self.driver.find_elements(By.TAG_NAME,"ifrmSeat"))
            self.driver.find_element(By.XPATH,"//*[@id='NextStepImage']").click()

        newthread = threading.Thread(target=task)
        newthread.start()

    # 결제
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

    def run_multiple_commands(self):
        # 여러 함수를 순차적으로 호출
        self.login()
        self.link_go()
        self.seat_select()
        self.payment()

app = App()
app.start()