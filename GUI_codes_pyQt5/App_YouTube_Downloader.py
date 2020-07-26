import os
import sys
import time
import threading
import urllib

from PyQt5.QtGui import QPixmap
from pytube import YouTube
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QPushButton


class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.folderPath = f"{os.path.expanduser('~')}/Desktop/유튜브 다운로드"

        # 변수 선언
        self.lb_title = QLabel(self)
        self.lb_time = QLabel(self)
        self.lb_thumb = QLabel(self)
        self.url_Edit = QLineEdit(self)
        self.url_btn = QPushButton('입력', self)
        self.lb_wait = QLabel("")

        # 다운로드 버튼 선언
        self.btn_labels = ["작업중 표시\n10초 동안 보기","저장위치 \n확인하기","컷편집\n미구현","gif 저장\n미구현"]
        self.btn1 = QPushButton(self.btn_labels[0],self)
        self.btn2 = QPushButton(self.btn_labels[1],self)
        self.btn3 = QPushButton(self.btn_labels[2],self)
        self.btn4 = QPushButton(self.btn_labels[3],self)
        self.btns = [self.btn1,self.btn2,self.btn3,self.btn4]
        self.btn_group = self.CreateBtnGroup()

        # 이벤트 연결
        self.url_btn.clicked.connect(lambda: self.AsignURL(self.url_Edit.text()))
        self.url_Edit.returnPressed.connect(lambda: self.AsignURL(self.url_Edit.text()))
        self.btn1.clicked.connect(lambda: self.onClick(0))
        self.btn2.clicked.connect(lambda: self.onClick(1))
        self.btn3.clicked.connect(lambda: self.onClick(2))
        self.btn4.clicked.connect(lambda: self.onClick(3))

        # 창 관련
        self.setLayout(self.Grid())
        self.setWindowTitle('YouTube Downloader')
        self.move(800, 300)
        self.resize(500, 200)
        self.show()

    #UI 관련
    def CreateBtnGroup(self):
        groupbox = QGroupBox('다운로드')
        # 버튼 위치시키기
        hbox = QHBoxLayout()
        hbox.addWidget(self.btn1)
        hbox.addWidget(self.btn2)
        hbox.addWidget(self.btn3)
        hbox.addWidget(self.btn4)
        groupbox.setLayout(hbox)
        return groupbox

    def Grid(self):
        grid = QGridLayout()
        grid.addWidget(QLabel('주소'), 0, 0)
        grid.addWidget(QLabel("제목"), 1, 0)
        grid.addWidget(QLabel("시간"), 2, 0)
        grid.addWidget(QLabel("사진"), 3, 0)
        grid.addWidget(self.url_Edit, 0, 1)
        grid.addWidget(self.url_btn, 0, 2)
        grid.addWidget(self.lb_title, 1, 1, 1, 1)
        grid.addWidget(self.lb_time, 2, 1, 1, 1)
        grid.addWidget(self.lb_thumb, 3, 1, 1, -1)
        grid.addWidget(self.btn_group, 4, 0, 1, -1)
        grid.addWidget(self.lb_wait, 5, 0, 1, -1)
        return grid

    # 이벤트 관련
    def AsignURL(self,url):
        if "https://www.youtube.com/" in url :
            t = threading.Thread(target=self.YouTube_object, args=(url,), daemon=True)
            t.start()
            threading.Thread(target=self.plz_wait, args=(t,self.url_btn), daemon=True).start()
        else:
            threading.Thread(target=self.url_error, daemon=True).start()

    def onClick(self, num):
        t = threading.Thread(target=self.download, args=(num,), daemon=True)
        t.start()
        threading.Thread(target=self.plz_wait, args=(t, self.btns[num]), daemon=True).start()

    # 콜백 함수
    def YouTube_object(self, url):
        try:
            self.yt = YouTube(url)
            self.yt_update(self.yt)
        except:
            self.debug(sys.exc_info()[0])

    def yt_update(self, yt):
        # 썸네일 읽기
        Pixmap_thumb = QPixmap()
        img_url = yt.thumbnail_url
        imageFromWeb = urllib.request.urlopen(img_url).read()
        Pixmap_thumb.loadFromData(imageFromWeb)
        Pixmap_thumb = Pixmap_thumb.scaledToWidth(600)

        # 라벨 갱신
        self.lb_title.setText(yt.title)
        self.lb_time.setText(f"{yt.length}초")
        self.lb_thumb.setPixmap(Pixmap_thumb)

        # 다운로드 버튼 관련
        self.yt_streams = yt.streams.filter(progressive=True, file_extension='mp4')  # mp4 확장자로 필터링

        # 버튼 생성
        self.btn_labels = [stream.resolution for stream in self.yt_streams]
        for i in range(4):
            btn = getattr(self,f"btn{i+1}")
            try: btn.setText(self.btn_labels[i]); btn.show()
            except: btn.hide()

    def download(self, num):
        folderPath = self.folderPath
        if not os.path.isdir(folderPath) : os.makedirs(folderPath)

        # 정상 작동할 떄
        try :
            target = self.yt_streams[num]
            target.download(folderPath)
            os.startfile(folderPath)
        # 주소가 유효하지 않을 떄
        except :
            if num == 0 :
                print(self.btns[num].text(),"start")
                time.sleep(10)
                print(self.btns[num].text(),"end")
            elif num ==1 :
                os.startfile(folderPath)

    # 편의 기능
    def plz_wait(self,t,btn):
        dots =""
        text = str(btn.text())
        ani = '̡ ̴̡ı̴̡̡ ̡͌l̡ ̴̡ı̴̴̡ ̡l̡ ̡ ̴̡ı̴̡̡ ̡͌l̡ ̴̡ı̴̴̡ ̡l̡ ̴̡ı̴̴̡ ̡̡͡ ̴̡ı̴̴̡ ̡̡͡|̲̲̲͡͡͡ ̲▫̲͡ ̲̲̲͡͡π̲̲͡͡ ̲̲͡▫̲̲͡͡ |̲̲̲͡͡͡ ̲▫̲͡ ̲̲̲͡͡π̲̲͡͡ ̲̲͡▫̲̲͡͡ ̲|̡̡̡>'
        w, f = len(ani), 3

        # 처리중 버튼 비활성화 및 표시
        btn.setEnabled(False)
        while t.is_alive() :
            dots += "."
            ani = ani[w-f:] + ani[:w-f]
            self.lb_wait.setText(text + dots + "\n" + ani*3)
            time.sleep(0.05)
            if len(dots) > 5 : dots = ""
        self.lb_wait.setText("작업완료")
        btn.setEnabled(True)
        time.sleep(2)
        self.lb_wait.setText("")

    def url_error(self):
        self.lb_wait.setText("잘못된 주소입니다."); time.sleep(1)
        self.lb_wait.setText("잘못된 주소입니다.\n정확한 주소를 입력해주세요."); time.sleep(2)
        self.lb_wait.setText("")

    def debug(self,obj):
        detail = dict(
            {"name":   [name for name in globals() if globals()[name] is obj],
             "type": type(obj),
             "vars": "-" * 40
             }, **vars(obj))
        white = max(map(len, detail.keys()))
        for x in detail: print(f"{x} {' ' * (white - len(x))} : {detail[x]} ")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())