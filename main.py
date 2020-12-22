from tkinter import *
import sys
import tkinter.ttk as ttk
import json
import os
import requests
import shutil
from threading import Thread
from zipfile import ZipFile

# Link para o update.zip
URL_UPDATE = 'https://baiak-ilusion.com/downloads/Baiak Ilusion Client Old.zip'
# Link para o server_info.json
URL_SERVER_INFO = 'https://raw.githubusercontent.com/nazesaria/ot_launcher_python/main/launcher_update/server_info.json'
# Senha .zip se existir no lugar de 123456, ou deixe como está
ZIP_PWD = b'123456'

# Execução do Launcher
class Launcher:

    local_dict = {}
    rede_dict = {}
    progress = 100
    buttons = ["Check", "Update", "Done!"]
    buttons_img = {'check': '', 'update': '', 'done': ''}
    receive_bytes = 0

    def __init__(self, root=Tk()):
        '''This class configures and populates the toplevel window.
           top is the toplevel containing window.'''
        _bgcolor = '#d9d9d9'  # X11 color: 'gray85'
        _fgcolor = '#000000'  # X11 color: 'black'
        _compcolor = '#d9d9d9' # X11 color: 'gray85'
        _ana1color = '#d9d9d9' # X11 color: 'gray85'
        _ana2color = '#ececec' # Closest X11 color: 'gray92'
        self.buttons_img['check'] = PhotoImage(file='./other/check_button.png')
        self.buttons_img['update'] = PhotoImage(file='./other/update_button.png')
        self.buttons_img['done'] = PhotoImage(file='./other/play_button.png')

        self.local_dict = self.loadFromJson("config.json")

        self.style = ttk.Style()
        if sys.platform == "win32":
            self.style.theme_use('winnative')
        self.style.configure('.',background=_bgcolor)
        self.style.configure('.',foreground=_fgcolor)
        self.style.map('.',background=[('selected', _compcolor), ('active',_ana2color)])
        self.style.configure("green.Horizontal.TProgressbar", background='green') # Cor da barra de progresso.

        root.geometry("800x500")
        root.minsize(120, 1)
        root.maxsize(1444, 881)
        root.resizable(1, 1)
        root.title("{} - Launcher".format(self.local_dict['Server Name']))
        root.configure(relief="groove")
        root.configure(background="#673434")
        root.resizable(width=False, height=False) # Proibe o redimensionamento da janela.

        self.menubar = Menu(root,font="TkMenuFont",bg=_bgcolor,fg=_fgcolor)
        root.configure(menu = self.menubar)

        self.TProgressbar = ttk.Progressbar(root, style='green.Horizontal.TProgressbar', length="682", value=self.progress)
        self.TProgressbar.place(relx=0.025, rely=0.92, relwidth=0.85, relheight=0.0, height=22)

        self.Label1 = Label(root, text='Current Version: {}'.format(self.local_dict['Version']), background="#673434")
        self.Label1.place(relx=0.025, rely=0.88, height=18, width=700)
        self.Label1.configure(disabledforeground="#a3a3a3", foreground="#000000")
        self.Label1.configure(justify=LEFT, anchor="w") # Posição texto

        self.Frame1 = Frame(root)
        self.Frame1.place(relx=0.025, rely=0.08, relheight=0.78, relwidth=0.95)
        self.Frame1.configure(relief='flat')
        self.Frame1.configure(borderwidth="2", background="#813e27")

        self.Button1 = Button(root, command=self.checkUpdate, image = self.buttons_img['check'], text=self.buttons[0], state='active', pady="0", highlightbackground="#d9d9d9", foreground="#000000", disabledforeground="#a3a3a3", background="#673434", activeforeground="#000000", activebackground="#ececec")
        self.Button1.place(relx=0.888, rely=0.92, height=24, width=70)
        self.Button1.configure(relief=GROOVE)
        root.mainloop()

    def downloadArchive(self, url, endereco=None):
        if endereco is None:
            endereco = os.path.basename(url.split("?")[0])
        resposta = requests.get(url, stream=True)
        if resposta.status_code == requests.codes.OK:
            if not os.path.exists('_tmp'):
                os.mkdir('_tmp')
            with open(f'_tmp/{endereco}', 'wb') as novo_arquivo:
                for parte in resposta.iter_content(chunk_size=256):
                    novo_arquivo.write(parte)
            return True
        else:
            return False

    def makeRedeDict(self):
        try:
            assert self.downloadArchive(URL_SERVER_INFO) == True
            self.rede_dict = self.loadFromJson('_tmp/server_info.json')
        except AssertionError:
            self.Label1['text'] = "Communication problem with the network when checking for update."
            self.Button1['image'] = self.buttons_img['done']
            self.Button1['command'] = self.playGame
            shutil.rmtree('./_tmp/', ignore_errors=True)

    def checkUpdate(self):
        self.makeRedeDict()
        try:
            if self.rede_dict['Version'] > self.local_dict['Version']:
                self.Button1['image'] = self.buttons_img['update']
                self.Button1['command'] = self.threadDownlaod
                self.TProgressbar['value'] = 0
                self.Label1['text'] = f"New Version Available: {self.rede_dict['Version']} "
            else:
                self.Button1['image'] = self.buttons_img['done']
                self.Button1['command'] = self.playGame
                shutil.rmtree('./_tmp/', ignore_errors=True)
        except KeyError:
            self.Label1['text'] = "Impossible to get value for new versions. Try restarting the launcher or communicating support."
            self.Button1['image'] = self.buttons_img['done']
            self.Button1['command'] = self.playGame
            shutil.rmtree('./_tmp/', ignore_errors=True)

    def threadDownlaod(self):
        self.Button1['state'] = DISABLED
        Thread(target = self.downloadUpdate).start()

    def downloadUpdate(self):
        response = requests.get(URL_UPDATE, stream=True)
        download = False
        if response.status_code == requests.codes.OK:
            if not os.path.exists('_tmp'):
                os.mkdir('_tmp')
            total_length = response.headers.get('content-length')
            # total_length = None
            with open('_tmp/update.zip', 'wb') as novo_arquivo:
                if total_length is None: # no content length header
                    total_length = 0
                else:
                    dl = 0
                    total_length = int(total_length)
                    for parte in response.iter_content(chunk_size=1024):
                        dl += len(parte)
                        self.TProgressbar['value'] = int(dl/total_length*100)
                        self.Label1['text'] = f"Downloading: {(dl/1000000):.2f}/{(total_length/1000000):.2f} Mbs, {self.TProgressbar['value']}%"
                        novo_arquivo.write(parte)
                    download = True
        if download:
            self.Label1['text'] = "Waiting for updates to be installed."
            self.descompactUpdate()
        else:
            self.Label1['text'] = "Communication problem with the network when checking for update."
            self.Button1['image'] = self.buttons_img['done']
            self.Button1['command'] = self.playGame
            self.Button1['state'] = ACTIVE

    def descompactUpdate(self):
        update = ZipFile('./_tmp/update.zip', 'r')
        update.extractall('.', pwd=ZIP_PWD)
        update.close()
        self.local_dict['Version'] = self.rede_dict['Version']
        self.writeDictFromJson('config.json')
        self.Button1['image'] = self.buttons_img['done']
        self.Button1['command'] = self.playGame
        self.Button1['state'] = ACTIVE
        self.Label1['text'] = f"Current Version: {self.rede_dict['Version']}"
        shutil.rmtree('./_tmp/', ignore_errors=True)

    def loadFromJson(self, file):
        with open(file, 'r') as archive:
            txt = archive.read()
            return json.loads(txt)

    def writeDictFromJson(self, file):
        with open(file, 'w') as arquivo:
            arquivo.write(json.dumps(self.local_dict, indent=2))

    def playGame(self):
        print('playGame')

launcher = Launcher()