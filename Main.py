import threading
class App(threading.Thread):
    super().__init__()
    def run_multiple_commands(self):
        # 여러 함수를 순차적으로 호출
        self.login()
        self.link_go()
        self.seat_select()
        self.payment()

app = App()
app.start()