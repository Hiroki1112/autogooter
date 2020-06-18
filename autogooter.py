import time,sys,os
from selenium import webdriver
import tkinter as tk
from functools import partial
from random import randint
from tkinter import messagebox
import threading

class Application(tk.Frame):
    
    def __init__(self,master):
        super().__init__(master)
        self.pack()

        self.master.geometry("500x500")
        self.master.title("Note 自動イイネ！")

        with open(self.resource_path('./data/config.csv')) as f:
            self.tmp = f.read()

        self.id,self.password = str(self.tmp).split(',')
        self.create_widgets()


    # Create Widgets function
    def create_widgets(self):
        
        self.label1 = tk.Label(text='note ID : ')
        self.label1.place(x=20,y=50)

        self.en1 = tk.Entry(width=40)
        self.en1.place(x=100,y=50)
        self.en1.insert(tk.END,self.id)

        self.label1 = tk.Label(text='パスワード : ')
        self.label1.place(x=20,y=80)

        self.en2 = tk.Entry(width=40)
        self.en2.place(x=100,y=80)
        self.en2.insert(tk.END,self.password)

        thread1 = threading.Thread(target=self.login)

        self.login = tk.Button(self.master,text="LOGIN",width=20,command=thread1.start)
        self.login.place(x=130, y=120)

        self.label3 = tk.Label(text='抽出対象URL : ')
        self.label3.place(x=20,y=170)

        self.en3 = tk.Entry(width=40)
        self.en3.place(x=100,y=170)

        self.label4 = tk.Label(text='イイネ数 : ')
        self.label4.place(x=20,y=200)

        self.en4 = tk.Entry(width=10)
        self.en4.place(x=100,y=200)
        self.en4.insert(tk.END,30)

        thread2 = threading.Thread(target=self.autoiine)

        self.iinestart = tk.Button(self.master,text="イイネStart!",width=20,command=thread2.start)
        self.iinestart.place(x=130, y=240)

    def resource_path(self,relative):
        if hasattr(sys, "_MEIPASS"):
            return os.path.join(sys._MEIPASS, relative)
        return os.path.join(relative)

    # Event Callback Function
    def login(self):
        self.driver = webdriver.Chrome(self.resource_path('./driver/chromedriver.exe'))
        url = "https://note.com/login"
        self.driver.get(url)
        time.sleep(4)
        id = self.driver.find_element_by_name('login')
        self.id = self.en1.get()
        id.send_keys(self.id)
        password = self.driver.find_element_by_name('password')
        self.password = self.en2.get()
        password.send_keys(self.password)
        log = self.driver.find_element_by_class_name('logining_msg').click()


    def autoiine(self):

        target = self.en3.get()
        self.driver.get(target)

        self.driver.find_element_by_class_name('o-timelineHome__moreButton').click()

        #targetClasses = self.driver.find_element_by_class_name('o-like')
        time.sleep(2)
        #for i in range(1,int(int(self.en4.get())/10)):
            #self.driver.execute_script("window.scrollTo(0, {})".format(i*3000))
            #time.sleep(2+randint(0,2))

        for i in range(int(self.en4.get())):
            self.driver.find_elements_by_class_name('o-like')[i].click()
            time.sleep(2+randint(0,4))
        
        messagebox.showinfo("イイネ終了","イイネが終了しました。")


def main():
    root = tk.Tk()
    app = Application(master=root)#Inheritクラスの継承！
    app.mainloop()

if __name__ == "__main__":
    main()