import malddal
import tkinter as tk
from threading import Thread, Semaphore
from tkinter import messagebox

global version
version = "v0.8.5"

global directory
directory = r'%systemdrive%\user\%username%\desktop'



if __name__ == '__main__':
    flag = False

    mymalddal = malddal.malddal()
    flagSem = mymalddal.getflagsem()
    gamepub, resize, is_top, korean_mode = mymalddal.getGameFrom()
    windowflag = False
    print(gamepub)

    if gamepub == 0:
        hwnd = mymalddal.getHwndOfDMM()
    else:
        hwnd = mymalddal.getHwndOfBluestacks()

    if resize:
        mymalddal.request_admin_and_resize(hwnd)
        exit(0)

    charScriptSpec, charScript, charSpec, charIter, charIter2 = mymalddal.read_script(korean_mode)
    charSkillSpec, charSkill, charSpecOfSkill = mymalddal.read_skill()


    window = tk.Tk()
    window.title("MALDDAL - DCInside 우마무스메 갤러리 " + version)
    window.minsize(500, 500)
    window.iconbitmap('malddal.ico')
    if is_top:
        window.attributes("-topmost", 1)

    def EXIT():
        flagSem.acquire()
        global flag
        flag = True
        flagSem.release()
        ocrThread.join()
        window.destroy()
        exit(0)

    window.protocol('WM_DELETE_WINDOW', EXIT)

    def EXITCheck():
        flagSem.acquire()
        global flag
        if flag:
            print("PROGRAM KILL DETECTED")
            exit(0)
        flagSem.release()

    scriptText = []
    specText = []
    message = tk.StringVar()
    for i in range(5):
        text = tk.StringVar()
        text2 = tk.StringVar()
        text.set("N/A")
        text2.set("N/A")
        scriptText.append(text)
        specText.append(text2)

    script0 = tk.Label(window, textvariable=scriptText[0], height=5, width=35, relief="groove")
    script1 = tk.Label(window, textvariable=scriptText[1], height=5, width=35, relief="groove")
    script2 = tk.Label(window, textvariable=scriptText[2], height=5, width=35, relief="groove")
    script3 = tk.Label(window, textvariable=scriptText[3], height=5, width=35, relief="groove")
    script4 = tk.Label(window, textvariable=scriptText[4], height=5, width=35, relief="groove")
    script5 = tk.Label(window)
    spec0 = tk.Label(window, textvariable=specText[0], height=5, width=50, relief="groove")
    spec0.bind("<Button-1>", lambda e: mymalddal.get_skill_info(specText[0], charSkillSpec, charSkill, charSpecOfSkill))
    spec1 = tk.Label(window, textvariable=specText[1], height=5, width=50, relief="groove")
    spec1.bind("<Button-1>", lambda e: mymalddal.get_skill_info(specText[1], charSkillSpec, charSkill, charSpecOfSkill))
    spec2 = tk.Label(window, textvariable=specText[2], height=5, width=50, relief="groove")
    spec2.bind("<Button-1>", lambda e: mymalddal.get_skill_info(specText[2], charSkillSpec, charSkill, charSpecOfSkill))
    spec3 = tk.Label(window, textvariable=specText[3], height=5, width=50, relief="groove")
    spec3.bind("<Button-1>", lambda e: mymalddal.get_skill_info(specText[3], charSkillSpec, charSkill, charSpecOfSkill))
    spec4 = tk.Label(window, textvariable=specText[4], height=5, width=50, relief="groove")
    spec4.bind("<Button-1>", lambda e: mymalddal.get_skill_info(specText[4], charSkillSpec, charSkill, charSpecOfSkill))
    spec5 = tk.Label(window, textvariable=message)

    def directory_button_click(dir):
        global directory
        directory = mymalddal.get_directory(dir)


    button0 = tk.Button(window, text="이미지 저장경로 변경",
                        command=lambda: directory_button_click(directory), width=20, height=3)

    def imagecapture(directory):
        rgb, temp = mymalddal.getWindowsImage(hwnd, gamepub)
        if mymalddal.game_capture(rgb, directory):
            message.set("저장 실패")
            window.after(2000, lambda: message.set(""))
        else:
            message.set(directory + " <- 저장 완료")
            window.after(2000, lambda: message.set(""))

    button1 = tk.Button(window, text="게임 캡쳐",
                        command=lambda: imagecapture(directory), width=20, height=3)

    script0.grid(row=0, column=0)
    script1.grid(row=1, column=0)
    script2.grid(row=2, column=0)
    script3.grid(row=3, column=0)
    script4.grid(row=4, column=0)
    script5.grid(row=5, column=0)
    button0.grid(row=6, column=0)
    spec0.grid(row=0, column=1)
    spec1.grid(row=1, column=1)
    spec2.grid(row=2, column=1)
    spec3.grid(row=3, column=1)
    spec4.grid(row=4, column=1)
    spec5.grid(row=5, column=1)
    button1.grid(row=6, column=1)


    def mainloop():
        lastPrinted = 99999
        while True:
            EXITCheck()
            global image
            global cap
            image, cap = mymalddal.getWindowsImage(hwnd, gamepub)
            script, spec, printed = mymalddal.OCR(cap, lastPrinted, charScriptSpec, charScript, charSpec, charIter,
                                                  charIter2)
            if lastPrinted == printed:
                continue
            lastPrinted = printed
            scriptIter = 0
            EXITCheck()
            for sc in script:
                flagSem.acquire()
                scriptText[scriptIter].set(sc)
                flagSem.release()
                scriptIter = scriptIter + 1
            for sc in range(scriptIter, 5):
                flagSem.acquire()
                scriptText[sc].set("N/A")
                flagSem.release()
            scriptIter = 0
            for sp in spec:
                flagSem.acquire()
                specText[scriptIter].set(sp)
                flagSem.release()
                scriptIter = scriptIter + 1
            for sc in range(scriptIter, 5):
                flagSem.acquire()
                specText[sc].set("N/A")
                flagSem.release()


    ocrThread = Thread(target=mainloop)
    ocrThread.start()
    window.mainloop()