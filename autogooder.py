import time,sys,os,signal
from selenium import webdriver
import tkinter as tk
from functools import partial
from random import randint
from tkinter import messagebox,filedialog
import threading
import requests

class Application(tk.Frame):
    
    def __init__(self,master):
        super().__init__(master)

        self.iinecount = 0

        self.pack()
        self.master.geometry("420x500")
        self.master.title("Note 自動イイネ！")

        with open(self.resource_path('./data/config.csv')) as f:
            self.tmp = f.read()

        self.id,self.password = str(self.tmp).split(',')
        self.create_widgets()
        
        #プログラムを起動してからイイネした数をカウントする
        


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

        #self.thread1 = threading.Thread(target=self.login)
        self.login = tk.Button(self.master,text="LOGIN",width=20,command=self.login)
        self.login.place(x=130, y=120)

        self.label3 = tk.Label(text='抽出対象URL : ')
        self.label3.place(x=20,y=170)

        self.en3 = tk.Entry(width=40)
        self.en3.place(x=100,y=170)

        self.label4 = tk.Label(text='イイネ数 : ')
        self.label4.place(x=20,y=200)

        self.label9 = tk.Label(text='今日のイイネ数 : {}'.format(self.iinecount))
        self.label9.place(x=170,y=200)

        self.en4 = tk.Entry(width=10)
        self.en4.place(x=100,y=200)
        self.en4.insert(tk.END,150)

        #self.thread2 = threading.Thread(target=self.autoiine)
        self.iinestart = tk.Button(self.master,text="イイネStart!",width=20,command=self.autoiine)
        self.iinestart.place(x=130, y=240)

        """
        self.label5 = tk.Label(text='ファイル選択 ')
        self.label5.place(x=20,y=300)
        
        self.selectButton = tk.Button(self.master,text="ファイルを選択する",width=12,command=self.select_file)
        self.selectButton.place(x=130, y=300)

        self.label6 = tk.Label(text='選択ファイル名 : ')
        self.label6.place(x=20,y=340)

        self.en5 = tk.Entry(width=40)
        self.en5.place(x=100,y=340)

        self.label7 = tk.Label(text='インターバル(秒) : ')
        self.label7.place(x=20,y=370)

        self.en6 = tk.Entry(width=10)
        self.en6.place(x=100,y=370)
        self.en6.insert(tk.END,300)

        self.label8 = tk.Label(text='イイネ数 : ')
        self.label8.place(x=20,y=400)

        self.en7 = tk.Entry(width=10)
        self.en7.place(x=100,y=400)
        self.en7.insert(tk.END,100)

        self.lumpstart = tk.Button(self.master,text="一括イイネstart",width=20,command=self.ikkatsuIIne)
        self.lumpstart.place(x=130, y=440)
        """
        self.label7 = tk.Label(text='検索ワード : ')
        self.label7.place(x=20,y=300)

        self.en6 = tk.Entry(width=10)
        self.en6.place(x=100,y=300)

        self.label8 = tk.Label(text='イイネ数 : ')
        self.label8.place(x=20,y=330)

        self.en7 = tk.Entry(width=10)
        self.en7.place(x=100,y=330)
        self.en7.insert(tk.END,150)

        self.lumpstart = tk.Button(self.master,text="検索イイネstart",width=20,command=self.search_iine)
        self.lumpstart.place(x=130, y=360)
    
    def search_iine(self):
        target = self.en6.get()
        self.driver.get("https://note.com/search?context=note&mode=search&q="+ target)

        time.sleep(2)

        for i in range(int(self.en4.get())):
            try:
                self.driver.find_elements_by_class_name('o-like')[i].click()
                time.sleep(2+randint(0,4))
                self.iinecount += 1
                
            
            except IndexError:
                messagebox.showinfo("IndexError:","{}件イイネしました.".format(i))
                break

            except KeyboardInterrupt:
                messagebox.showinfo("IndexError:","{}件イイネしました.".format(i))
                break
                    
        self.label9["text"] = '今日のイイネ数 : {}'.format(self.iinecount)
        messagebox.showinfo("イイネ終了","イイネが終了しました。")


    def select_file(self):
        fTyp = [("","*")]
        iDir = os.path.abspath(os.path.dirname(__file__))
        filepath = filedialog.askopenfilename(filetypes = fTyp,initialdir = iDir)
        self.en5.insert(tk.END,filepath)


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

        time.sleep(2)
        #for i in range(1,int(int(self.en4.get())/10)):
            #self.driver.execute_script("window.scrollTo(0, {})".format(i*3000))
            #time.sleep(2+randint(0,2))

        for i in range(int(self.en4.get())):
            try:
                self.driver.find_elements_by_class_name('o-like')[i].click()
                time.sleep(2+randint(0,4))
                self.iinecount += 1
                
            
            except IndexError:
                messagebox.showinfo("IndexError:","{}件イイネしました.".format(i))
                break

            except KeyboardInterrupt:
                messagebox.showinfo("IndexError:","{}件イイネしました.".format(i))
                break
                    
        self.label9["text"] = '今日のイイネ数 : {}'.format(self.iinecount)
        messagebox.showinfo("イイネ終了","イイネが終了しました。")
    
    def ikkatsuIIne(self):
        '''
        autoiineを使いまわしできるように設計しておくべきだった。
        作り直すのが面倒なので新しく関数を作成する。
        '''

        #ファイルの読み込み
        with open(self.en5.get()) as f:
            self.tmp2 = f.read()

        self.files = list(str(self.tmp2).split(','))
        print(self.files)

        for url in self.files:
            print(url)
            self.driver.get(url)

            self.driver.find_element_by_class_name('o-timelineHome__moreButton').click()
            #for i in range(1,int(int(self.en4.get())/10)):
                #self.driver.execute_script("window.scrollTo(0, {})".format(i*3000))
                #time.sleep(2+randint(0,2))

            for i in range(int(self.en7.get())):
                try:
                    self.driver.find_elements_by_class_name('o-like')[i].click()
                    time.sleep(2+randint(0,4))
                
                except IndexError:
                    break
            
            time.sleep(int(self.en6.get()))
            
        messagebox.showinfo("一括イイネ終了","イイネが終了しました。")

def main():
    root = tk.Tk()
    app = Application(master=root)#Inheritクラスの継承！
    app.mainloop()

if __name__ == "__main__":
    main()