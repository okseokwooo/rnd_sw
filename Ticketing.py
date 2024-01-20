import time
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument("--start-fullscreen")  # 배율을 1.5로 설정 (원하는 값으로 변경)
chrome_options.add_argument("--force-device-scale-factor=0.8")  # Set the device scale factor to 0.5
driver = webdriver.Chrome(options=chrome_options)


def close_popup(driver):
    try:
        popup_close_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="popup-prdGuide"]/div/div[3]/button'))
        )
        popup_close_button.click()
    except:
        pass

my_interpark_id = "oswzxc"
my_interpark_pw = "theone!23"
login_url = "https://ticket.interpark.com/Gate/TPLogin.asp" # 로그인 창
my_url = "https://tickets.interpark.com/goods/23012526" # 공연 URL

want_month = 1 # 원하는 월
want_day = 13 # 원하는 일
want_turn = 2 # 원하는 공연 회차 ( 1회 = 2시 , 2회 = 7 시)
want_floor = 3 # 원하는 관람 층 (1 = 1층, 2 = 2층, 3 = 3층)

driver.get(login_url)

iframes = driver.find_elements(By.TAG_NAME, "iframe")
driver.switch_to.frame(iframes[0])

time.sleep(0.2)
id_input = driver.find_element(By.CSS_SELECTOR, "#userId")
pw_input = driver.find_element(By.CSS_SELECTOR, "#userPwd")
id_input.send_keys(my_interpark_id)
time.sleep(0.2)
pw_input.send_keys(my_interpark_pw)
button = driver.find_element(By.CSS_SELECTOR, "#btn_login")
button.click()

driver.get(my_url)
time.sleep(0.3)

nxt_button = driver.find_element(By.XPATH, "//*[@id='productSide']/div/div[1]/div[1]/div[2]/div/div/div/div/ul[1]/li[3]")

# 팝업 닫기
close_popup(driver)

while True:
    current_date = driver.find_element(By.XPATH,"//*[@id='productSide']/div/div[1]/div[1]/div[2]/div/div/div/div/ul[1]/li[2]")
    cur_month = int(current_date.text.split(' ')[1])
    if cur_month != want_month:
        nxt_button.click()
        time.sleep(0.3)
    else:
        time.sleep(0.3)
        break

find_day = driver.find_element(By.XPATH, "//li[text()='"+str(want_day)+"']")
find_day.click()

turn_list = driver.find_elements(By.CLASS_NAME, "timeTableItem")
turn_list[want_turn - 1].click()

driver.switch_to.window(driver.window_handles[-1])

time.sleep(1)
driver.find_element(By.XPATH, '//*[@id="productSide"]/div/div[2]/a[1]').click()

time.sleep(1)

main_window_handle = driver.current_window_handle
all_window_handles = driver.window_handles
new_window_handle = [handle for handle in all_window_handles if handle != main_window_handle][0]
# 새 창으로 전환
driver.switch_to.window(new_window_handle)

iframes = driver.find_elements(By.TAG_NAME, "iframe")
for ifr in iframes:
    if ifr.get_attribute('name') == 'ifrmSeat':
        print("convert")
        driver.switch_to.frame(ifr)
        driver.switch_to.frame('ifrmSeatView')
        break

if want_floor != 1: # 2 or 3층
    Seat_region = driver.find_element(By.XPATH, "//*[@id='TmgsTable']/tbody/tr/td/map")
    area_element = Seat_region.find_element(By.TAG_NAME, "area")

    href_value = area_element.get_attribute("href")
    # href 값이 javascript:로 시작하는지 확인
    if href_value.startswith("javascript:"):
        driver.execute_script(href_value)
    time.sleep(0.5)

driver.switch_to.window(new_window_handle)
iframes = driver.find_elements(By.TAG_NAME, "iframe")

for ifr in iframes:
    if ifr.get_attribute('name') == 'ifrmSeat':
        driver.switch_to.frame(ifr)
        driver.switch_to.frame('ifrmSeatDetail')
        break

available_reserve_seat = driver.find_elements(By.XPATH, "//img[@class='stySeat']")

# 먹을수있는 자리를 먹어라
want_seat_cnt = 3 # 자리수
want_continue = 1 # 1 = 연석, 0 = 연석 상관 없음

flag = 0
want_seat_list = []
if want_continue == 1: # 연석 자리 잡기

    seat_map = [[[] for i in range(25)] for j in range(4)]
    seat_map_num = [[[] for i in range(25)] for j in range(4)]
    for seat in available_reserve_seat:
        _str = str(seat.get_attribute('alt')).split(' ')
        seat_floor = int(_str[1].split('-')[0].split('층')[0])
        if seat_floor == want_floor:
            seat_row = int(_str[1].split('-')[1].split('열')[0])
            seat_column = int(_str[1].split('-')[2])
            seat_map[seat_floor][seat_row].append(seat.get_attribute('alt'))
            seat_map_num[seat_floor][seat_row].append(seat_column)

    for row in range(25): # 열
        _size = len(seat_map[want_floor][row])
        if _size >= want_seat_cnt: # 해당 층의 열에 원하는 연석 자리수 이상있어야함
            for i in range(0, _size - want_seat_cnt):
                ret = 0 # 현재 열에서 k 자리 연석이 있냐?
                pre_num = seat_map_num[want_floor][row][i] - 1
                for k in range(want_seat_cnt):
                    if seat_map_num[want_floor][row][i+k] == pre_num + 1:
                        ret += 1
                        pre_num += 1
                    else:
                        break

            if ret == want_seat_cnt:
                for k in range(want_seat_cnt):
                    want_seat_list.append(seat_map[want_floor][row][i+k])
                flag = 1
                break
        if flag == 1:
            break

else:
    ret = 0
    for seat in available_reserve_seat:
        want_seat_list.append(seat)
        ret = ret + 1
        if ret == want_seat_cnt:
            flag = 1
            break

if flag == 1:
    for str in want_seat_list:
        b1 = driver.find_element(By.XPATH,"//img[@alt='"+str+"']")
        b1.click()

    driver.switch_to.window(new_window_handle)
    iframes = driver.find_elements(By.TAG_NAME, "iframe")

    for ifr in iframes:
        if ifr.get_attribute('name') == 'ifrmSeat':
            driver.switch_to.frame(ifr)
            break

    select_button = driver.find_element(By.XPATH, "//*[@id='NextStepImage']")
    select_button.click()

time.sleep(10)
driver.switch_to.default_content()
driver.quit()