import win32gui
import numpy as np
from PIL import ImageGrab, Image
import pytesseract
import tkinter as tk
from tkinter import messagebox, filedialog
from screeninfo import get_monitors
import ctypes, sys
import pandas as pd
import xlrd
import time

# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


class malddal:

    def __init__(self) -> None:
        super().__init__()
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'
        try:
            print(pytesseract.get_tesseract_version())
        except pytesseract.pytesseract.TesseractNotFoundError:
            messagebox.showinfo(title="tesseract 에러", message="tesseract OCR 프로그램을 감지 할 수 없습니다.")
            exit(0)

    def destroyWindow(self):
        exit(0)

    def getGameFrom(self):
        window = tk.Tk()
        window.title("프로그램 옵션")
        window.geometry('300x200')
        window.protocol('WM_DELETE_WINDOW', self.destroyWindow)
        window.iconbitmap('malddal.ico')
        radio_value = tk.IntVar()
        check_value = tk.BooleanVar()

        radio_button1 = tk.Radiobutton(window, text='  DMM  ', variable=radio_value, value=0)
        # radio_button2 = tk.Radiobutton(window, text='bluestack', variable=self.radio_value, value=1)
        radio_button1.pack(pady=20)
        # radio_button2.pack()

        checkbox = tk.Checkbutton(window, text='최적 해상도 변경', variable=check_value)
        checkbox.pack(pady=10)

        def clickOK():
            window.destroy()

        button = tk.Button(window, text="확인", command=clickOK, width=15, height=3)

        button.pack(pady=5)

        window.mainloop()
        return radio_value.get(), check_value.get()

    def getHwndOfDMM(self):
        return win32gui.FindWindow(None, "umamusume")

    def getHwndOfBluestack(self):
        return win32gui.FindWindow(None, "")

    def getWindowsImage(self, hwnd):
        try:
            rgb = np.array(ImageGrab.grab(bbox=win32gui.GetWindowRect(hwnd), all_screens=True))
        except:
            messagebox.showinfo(title="Game not found", message="게임을 찾을 수 없었습니다. 게임을 먼저 실행후 실행하십시오. \n프로그램 재시작이 필요합니다.")
            exit(0)
        rgb = np.delete(rgb, range(9 + 22), axis=0).copy()
        rgb = np.delete(rgb, range(9), axis=1).copy()
        rgb = np.delete(rgb, range(rgb.shape[0] - 9, rgb.shape[0]), axis=0).copy()
        rgb = np.delete(rgb, range(rgb.shape[1] - 9, rgb.shape[1]), axis=1).copy()

        cap = np.delete(rgb, range(int(rgb.shape[0] / 4.5)), axis=0).copy()
        cap = np.delete(cap, range(int(cap.shape[0] * 0.6), cap.shape[0]), axis=0).copy()
        cap = np.delete(cap, range(int(rgb.shape[1] / 10)), axis=1).copy()
        return rgb, cap

    def resizeWindow(self, hwnd):
        x0, y0, x1, y1 = win32gui.GetWindowRect(hwnd)
        monitor = get_monitors()
        target_width = 540
        target_height = 960
        win32gui.MoveWindow(hwnd, x0, y0, target_width, target_height, True)

    def leven(self, aText, bText):
        aLen = len(aText) + 1
        bLen = len(bText) + 1
        array = [[] for a in range(aLen)]
        for i in range(aLen):
            array[i] = [0 for a in range(bLen)]
        for i in range(bLen):
            array[0][i] = i
        for i in range(aLen):
            array[i][0] = i
        cost = 0
        for i in range(1, aLen):
            for j in range(1, bLen):
                if aText[i - 1] != bText[j - 1]:
                    cost = 1
                else:
                    cost = 0
                addNum = array[i - 1][j] + 1
                minusNum = array[i][j - 1] + 1
                modiNum = array[i - 1][j - 1] + cost
                minNum = min([addNum, minusNum, modiNum])
                array[i][j] = minNum
        return array[aLen - 1][bLen - 1]

    def is_admin(self):
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False

    def OCR(self, image, lastPrinted, charScriptSpec, charScript, charSpec, charIter, charIter2):
        try:
            ocrOut = pytesseract.image_to_boxes(image, lang='jpn')
            print(ocrOut)
        except pytesseract.pytesseract.TesseractError:
            messagebox.showinfo(title="OCR language ERR", message="tesseract 에 일본어팩이 포함되어 있지 않습니다.")
            exit(0)
        ocrScript = ocrOut.split('\n')

        entryScript = ""
        found = False
        for script in ocrScript:
            if len(script) >= 2:
                # 자주 잡히는 OCR Error 수정 하드코딩
                script = script.replace("/", "！")
                script = script.replace("7", "！")
                print(script)
                revenList = []
                for charSc in charScript:
                    forAppend = self.leven(charSc, script)
                    revenList.append(forAppend)
                index = revenList.index(min(revenList))
                if min(revenList) < 4:
                    if len(charScript[index]) == min(revenList):
                        continue
                    found = True
                    break;
        ScriptforPrint = []
        SpecforPrint = []
        if found:
            charIt = charIter[index]
            startIndex = charIter.index(charIt)
            nowPrinted = startIndex
            if startIndex != lastPrinted:
                ScriptforPrint.append(charScript[startIndex])
                SpecforPrint.append(charSpec[startIndex].replace("&", "\n"))
                startIndex = startIndex + 1
                while charIter2[startIndex] != 1:
                    ScriptforPrint.append(charScript[startIndex])
                    SpecforPrint.append(charSpec[startIndex].replace("&", "\n"))
                    startIndex = startIndex + 1
        else:
            nowPrinted = lastPrinted
        return ScriptforPrint, SpecforPrint, nowPrinted


    def request_admin_and_resize(self, hwnd):
        if self.is_admin():
            self.resizeWindow(hwnd)
        else:
            def destroyWindow():
                exit(0)

            def clickNoGo():
                window.destroy()

            def clickGo():
                # 관리자 권한으로 프로그램을 새로 실행하고 현제 프로그램 종료
                window.destroy()
                ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
                exit(0)

            window = tk.Tk()
            window.title("관리자 권한 필요")
            window.geometry('350x250')
            window.protocol('WM_DELETE_WINDOW', destroyWindow)
            label = tk.Label(window, text="최적 크기로 변경하려면 관리자권한으로 실행해야합니다.")
            label.pack(pady='20')
            button2 = tk.Button(window, text="크기 변경 하지 않음", command=clickNoGo, width=15, height=3)
            button = tk.Button(window, text="권한 요청 및 재실행", command=clickGo, width=15, height=3)
            button2.pack(pady='20')
            button.pack(pady='20')
            window.mainloop()

    def read_script(self):
        df = pd.read_excel('./character_script_spec.xls')
        charScriptSpec = df.values.tolist()
        charScript = [script[1] for script in charScriptSpec]
        charSpec = [spec[2] for spec in charScriptSpec]
        charIter = [it[3] for it in charScriptSpec]
        charIter2 = [it[4] for it in charScriptSpec]

        return charScriptSpec, charScript, charSpec, charIter, charIter2


    def get_directory(self, directory):
        window = tk.Tk()
        window.withdraw()
        path = filedialog.askdirectory(parent=window, initialdir=directory, title="이미지 저장 경로 설정")
        return path

    def game_capture(self, image, path):
        try:
            forSave = Image.fromarray(image)
            fulldir = path + "/" + time.strftime("%Y%m%d-%H%M%S") + ".jpeg"
            fulldir = fulldir.replace("/", '\\')
            forSave.save(str(fulldir))
            return 0
        except OSError:
            return 1
