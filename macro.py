import ntplib
from time import localtime, sleep
import os
import datetime
from tkinter import *
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options

class App():
    def __init__(self):
        super().__init__()
        chrome_options = Options()
        chrome_options.add_argument("--start-maximized")  # 최대화 옵션 추가
        self.driver = webdriver.Chrome(options=chrome_options)
        self.wait = WebDriverWait(self.driver, 10)
        self.url = "https://ticket.interpark.com/Gate/TPLogin.asp"
        self.driver.get(self.url)

        self.window = Tk()
        self.window.title("Interpark Ticketing Program")
        self.window.geometry("500x500")

        self.object_frame = Frame(self.window, bg="#f0f0f0")
        self.object_frame.pack(padx=20, pady=20)

        # Hour 입력
        self.hour_label = Label(self.object_frame, text="Hour", bg="#f0f0f0", fg="#333333", font=("Arial", 12))
        self.hour_label.grid(row=0, column=0, padx=5, pady=5)
        self.hour_entry = Spinbox(self.object_frame, from_=0, to=23, width=5, font=("Arial", 12))
        self.hour_entry.grid(row=0, column=1, padx=5, pady=5)

        # Min 입력
        self.min_label = Label(self.object_frame, text="Min", bg="#f0f0f0", fg="#333333", font=("Arial", 12))
        self.min_label.grid(row=0, column=2, padx=5, pady=5)
        self.min_entry = Spinbox(self.object_frame, from_=0, to=59, width=5, font=("Arial", 12))
        self.min_entry.grid(row=0, column=3, padx=5, pady=5)

        self.labels = ["ID", "Password", "Showcode", "Month", "Date", "Round", "Seat", "Birth"]
        self.entries = {}

        for i, label_text in enumerate(self.labels):
            label = Label(self.object_frame, text=label_text, bg="#f0f0f0", fg="#333333", font=("Arial", 12))
            label.grid(row=i+1, column=0, sticky="e", padx=5, pady=5)

            entry = Entry(self.object_frame, width=30, font=("Arial", 12))
            entry.grid(row=i+1, column=1, columnspan=3, padx=5, pady=5)
            self.entries[label_text] = entry

        self.bank_var = IntVar(value=0)
        self.bank_check = Checkbutton(self.object_frame, text='무통장', variable=self.bank_var, bg="#f0f0f0", font=("Arial", 12))
        self.bank_check.grid(row=len(self.labels)+1, column=1, padx=5, pady=5, sticky="w")

        self.kakao_var = IntVar(value=0)
        self.kakao_check = Checkbutton(self.object_frame, text='카카오', variable=self.kakao_var, bg="#f0f0f0", font=("Arial", 12))
        self.kakao_check.grid(row=len(self.labels)+1, column=2, padx=5, pady=5, sticky="w")

        self.commit_button = Button(self.object_frame, text="Commit", width=15, height=2, command=self.login, bg="#007bff", fg="#ffffff", font=("Arial", 12, "bold"))
        self.commit_button.grid(row=len(self.labels)+2, column=1, columnspan=2, pady=10)

        self.window.mainloop()

    #Login
    def login(self):
        try:
            self.iframe = self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "iframe")))
            self.driver.switch_to.frame(self.iframe)
            self.driver.find_element(By.CSS_SELECTOR, "#userId").send_keys(self.entries["ID"].get())
            self.driver.find_element(By.CSS_SELECTOR, "#userPwd").send_keys(self.entries["Password"].get())
            self.driver.find_element(By.CSS_SELECTOR, "#btn_login").click()
            self.waittime()
        except NoSuchElementException:
            print("로그인 요소를 찾을 수 없음")
        finally:
            self.driver.switch_to.default_content()

    def waittime(self):
        target_hour = int(self.hour_entry.get())
        target_minute = int(self.min_entry.get())
    
        def get_ntp_time():
            ntp_client = ntplib.NTPClient()
            response = ntp_client.request('pool.ntp.org')
            return response.tx_time
    
        def is_time_to_run_code(target_hour, target_minute):
            current_time = datetime.datetime.now()
            return current_time.hour == target_hour and current_time.minute == target_minute and current_time.second == 0
    
        while True:
            if is_time_to_run_code(target_hour, target_minute):
                self.link_go()
                break
            else:
                sleep(1)

    def link_go(self):
        self.driver.get('http://poticket.interpark.com/Book/BookSession.asp?GroupCode=' + self.entries["Showcode"].get())
        self.date_select()

    def date_select(self):
        while True:
            try:
                self.driver.switch_to.frame(self.driver.find_element_by_id('ifrmBookStep'))
                if self.entries["Month"].get() == 0:
                    pass
                elif self.entries["Month"].get() >= 1:
                    for i in range(1, int(self.entries["Month"].get()) + 1):
                        self.driver.find_element_by_xpath("/html/body/div/div[1]/div[1]/div/span[3]").click()
                try:
                    self.driver.find_element_by_xpath(
                        '(//*[@id="CellPlayDate"])' + "[" + self.entries["Date"].get() + "]").click()
                    break
                except NoSuchElementException:
                    self.link_go()
                    break
            except NoSuchElementException:
                self.link_go()
                break
    
        self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, '/html/body/div/div[3]/div[1]/div/span/ul/li[' + self.entries["Round"].get() + ']/a'))).click()
        self.driver.switch_to.default_content()
        self.driver.find_element_by_id('LargeNextBtnImage').click()

app = App()