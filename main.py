import requests
from bs4 import BeautifulSoup
from tkinter import filedialog
from tkinter import *
import re
from PIL import Image, ImageTk
from threading import Thread
class Scraper:
    def __init__(self):
        self.headers = {"User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36"}
        self.textToSearch = 'https://www.myvideo.ge/Scripts/mvplayer/3.0/anotations.js'
        self.createRoot()
        self.create_elements()
        self.init_elements()

    def downloader(self,url,filename):
        mainTag = ''

        resposne = requests.get(url,headers=self.headers)
        soup = BeautifulSoup(resposne.text,"html.parser")
        scriptTags = soup.find("div", class_="mv_video_player_cont").div.find_all("script")
        for scriptTag in scriptTags:
            if str(scriptTag).find(self.textToSearch) >=0 :
                # csoup = BeautifulSoup(str(scriptTag), 'lxml')
                # print(csoup.find("re.search"))
                videoUrl = re.findall(r"file.*.\"",str(scriptTag))[0].split('file:')[1].replace('"',"").replace(" ","")
                video = requests.get(videoUrl,headers=self.headers)
                file = open(str(self.folder_path)+"/"+str(filename)+".mp4","wb")
                print("begin")
                with file:
                    file.write(video.content)
                file.close()
                self.idle()
                print(str(self.folder_path)+str(filename))
                return

        return
    def progress(self):
        self.folder_path = filedialog.askdirectory()
        print(self.folder_path)
        url = self.url.get()
        fileName = self.fileName.get()
        if not url or not fileName:
            return
        self.button.config({"text":"Downloading","state":DISABLED})

        Thread(target=self.downloader,args=[url,fileName]).start()
        return
    def idle(self):
        self.button.config({"text":"Download","state":ACTIVE})

    def create_elements(self):

        load = Image.open("./images/icon.png")
        render = ImageTk.PhotoImage(load)
        self.imageLabel = Label(self.root, image=render, bg="#002c38")
        self.imageLabel.image = render

        self.folder_path = StringVar()
        self.fileNameLabel = Label(self.root, text="Name for the file ",justify="center",bg="#002c38",fg="white")
        self.urlLabel = Label(self.root, text="Video Url",justify="center", bg="#002c38",fg="white")

        self.url = Entry(self.root, borderwidth=0,   font="Arial 9 ")
        self.fileName = Entry(self.root, borderwidth=0,  font="Arial 11 ")
        self.button = Button(self.root, cursor="hand2", borderwidth=0, text="Download", bg="#a5181c", fg="white",activebackground="#a5181c", activeforeground="white", font="Arial 12 bold", command=lambda: Thread(target=self.progress).start())

        self.infolabel = Label(self.root,fg="white",bg="#002c38",text="Download the videos from MYVIDEO.GE.\n file name will save file with that name on the path you have chosen,\n url is video url like this one: https://myvideo.ge/v/578873")
    def init_elements(self):
        self.imageLabel.pack(pady=10)

        self.fileNameLabel.pack(fill=X, pady=1)
        self.fileName.pack(fill=X, ipady=8, pady=3, padx=8)

        self.urlLabel.pack(fill=X,  pady=1)
        self.url.pack(fill=X, ipady=8, pady=3, padx=8)

        self.button.pack(fill=X,ipady=10,pady=3, padx=8)
        self.infolabel.pack(fill=X,pady=5)
    def createRoot(self):
        windowWidth = 400
        windowHeight = 400
        self.root = Tk()  # main tkinter object
        self.root.geometry(str(windowWidth) + 'x' + str(windowHeight))
        self.root.configure(bg='#002c38')
        self.root.resizable(False, False)
        self.root.title("Myvideo Downloader");
        self.root.iconbitmap(r'./images/icon.ico');


    def run(self):
        self.root.mainloop()



if __name__ == "__main__":
    scraper = Scraper()
    scraper.run()