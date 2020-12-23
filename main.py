from tkinter import *
import tkinter.font as tkFont
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
        self.buttons_img['check'] = PhotoImage(file='data/check_button.png')
        self.buttons_img['update'] = PhotoImage(file='data/update_button.png')
        self.buttons_img['done'] = PhotoImage(file='data/play_button.png')
        self.patch_logo = PhotoImage(file='data/patch_logo.png')
        self.local_dict = self.loadFromJson("data/config.json")

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
        root.configure(background="#303030")
        root.resizable(width=False, height=False) # Proibe o redimensionamento da janela.

        self.menubar = Menu(root,font="TkMenuFont",bg=_bgcolor,fg=_fgcolor)
        root.configure(menu = self.menubar)

        self.TProgressbar = ttk.Progressbar(root, style='green.Horizontal.TProgressbar', length="682", value=self.progress)
        self.TProgressbar.place(relx=0.025, rely=0.92, relwidth=0.85, relheight=0.0, height=22)

        self.Label1 = Text(root, background="#303030", font=("Arial", "9", "bold"), foreground = '#ffffff')
        self.Label1.place(relx=0.025, rely=0.87, height=25, width=700)
        # self.Label1.configure(disabledforeground="#a3a3a3", foreground="#ffffff")
        self.Label1.insert(END, 'Current Version: {}'.format(self.local_dict['Version']))
        self.Label1.configure(relief = 'flat', state = DISABLED) # Posição texto

        self.Frame1 = Frame(root, width=760,height=345)
        self.Frame1.place(relx=0.025, rely=0.15, relheight=0.7, relwidth=0.95)
        self.Frame1.configure(relief='flat')
        self.Frame1.configure(borderwidth="2", background="#303030")

        self.Canvas = Canvas(self.Frame1, relief='flat')
        self.Canvas.configure(borderwidth="0", background="#000000", scrollregion=(0,0,0,1000))

        self.VScrollBar = Scrollbar(self.Frame1, orient = VERTICAL, background = '#000000', bd = 0,  troughcolor='#000000', highlightcolor = '#000000', highlightbackground='#000000')
        # self.VScrollBar.pack(side = RIGHT, fill = Y) # Ativar Barra de Scroll
        self.VScrollBar.config(command=self.Canvas.yview)

        self.Canvas.config(width = 760, height = 345)
        self.Canvas.config(yscrollcommand=self.VScrollBar.set)
        self.Canvas.pack(side = LEFT, expand = True, fill = BOTH)
        self.Canvas.bind('<Enter>', self._bound_to_mousewheel)
        self.Canvas.bind('<Leave>', self._unbound_to_mousewheel)

        self.PatchLogo = Label(root, image=self.patch_logo, background='#000000')
        self.PatchLogo.place(relx = 0.55, rely = 0.158, relheight = 0.685, relwidth = 0.42)

        self.Credit = Message(root, text = '''Launcher created by Naze#3578.''', width = 250, bg = "#303030", foreground = '#464646', highlightbackground = '#d9d9d9', highlightcolor = '#000000')
        self.Credit.place(relx = 0.775, rely = 0.961, relheight = 0.040, relwidth = 0.23)

        self.Button1 = Button(root, command=self.checkUpdate, image = self.buttons_img['check'], text=self.buttons[0], state='active', pady="0", highlightbackground="#d9d9d9", foreground="#000000", disabledforeground="#a3a3a3", background="#673434", activeforeground="#000000", activebackground="#ececec")
        self.Button1.place(relx=0.888, rely=0.92, height=24, width=70)
        self.Button1.configure(relief=GROOVE)

        # Make Patch Note
        self.makePatchTitle(0, "Patch Note: Version {}".format(self.local_dict['Version']))
        self.makePatchNote(0, 'Maximo adequado 100 caracteres... Maximo adequado 100 caracteres... Maximo adequado 100 caracteres...')
        self.makePatchNote(1, 'Maximo adequado 100 caracteres... Maximo adequado 100 caracteres... Maximo adequado 100 caracteres...')
        self.makePatchNote(2, 'Maximo adequado 100 caracteres... Maximo adequado 100 caracteres... Maximo adequado 100 caracteres...')
        self.makePatchNote(3, 'Maximo adequado 100 caracteres... Maximo adequado 100 caracteres... Maximo adequado 100 caracteres...')
        self.makePatchNote(4, 'Maximo adequado 100 caracteres... Maximo adequado 100 caracteres... Maximo adequado 100 caracteres...')
        self.makePatchNote(5, 'Maximo adequado 100 caracteres... Maximo adequado 100 caracteres... Maximo adequado 100 caracteres...')
        self.makePatchSeparator(7)
        self.makePatchTitle(8, "Patch Note: Version {}".format(self.local_dict['Version']))
        self.makePatchNote(8, 'Maximo adequado 100 caracteres... Maximo adequado 100 caracteres... Maximo adequado 100 caracteres...')
        self.makePatchNote(9, 'Maximo adequado 100 caracteres... Maximo adequado 100 caracteres... Maximo adequado 100 caracteres...')
        self.makePatchNote(10, 'Maximo adequado 100 caracteres... Maximo adequado 100 caracteres... Maximo adequado 100 caracteres...')
        self.makePatchNote(11, 'Maximo adequado 100 caracteres... Maximo adequado 100 caracteres... Maximo adequado 100 caracteres...')
        self.makePatchNote(12, 'Maximo adequado 100 caracteres... Maximo adequado 100 caracteres... Maximo adequado 100 caracteres...')
        self.makePatchNote(13, 'Maximo adequado 100 caracteres... Maximo adequado 100 caracteres... Maximo adequado 100 caracteres...')

        root.mainloop()

    def makePatchTitle(self, n, title, color = 'white'):
        factor = 43 * n
        self.Canvas.create_text(150,20+factor, fill=color, font="Georgia 16 bold",text=title)

    def makePatchNote(self, n, txt, color = 'white', border = '#303030', background = '#2c2c2c'):
        factor = 43 * n
        self.Canvas.create_polygon([50,75+factor,50,40+factor,400,40+factor,400,75+factor], outline=border, fill=background, width=2)
        self.Canvas.create_text(55,42+factor, fill=color, font="Georgia 10",text=txt, anchor='nw', width = 350)
    
    def makePatchSeparator(self, n):
        factor = 43 * n
        self.Canvas.create_polygon([0,40+factor,0,40+factor,600,40+factor,600,40+factor], outline='white', fill='white', width=2)

    def _bound_to_mousewheel(self, event):
        self.Canvas.bind_all("<MouseWheel>", self._on_mousewheel)   

    def _unbound_to_mousewheel(self, event):
        self.Canvas.unbind_all("<MouseWheel>")

    def _on_mousewheel(self, event):
        self.Canvas.yview_scroll(int(-1*(event.delta/120)), "units")

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
            self.insertLabelText('Communication problem with the network when checking for update.')
            self.Button1['image'] = self.buttons_img['done']
            self.Button1['command'] = self.playGame
            shutil.rmtree('./_tmp/', ignore_errors=True)

    def insertLabelText(self, text):
        self.Label1.configure(state = NORMAL)
        self.Label1.delete(1.0, END)
        self.Label1.insert(END, text)
        self.Label1.configure(state = DISABLED)

    def checkUpdate(self):
        self.makeRedeDict()
        try:
            if self.rede_dict['Version'] > self.local_dict['Version']:
                self.Button1['image'] = self.buttons_img['update']
                self.Button1['command'] = self.threadDownlaod
                self.TProgressbar['value'] = 0
                self.insertLabelText(f"New Version Available: {self.rede_dict['Version']}")
            else:
                self.Button1['image'] = self.buttons_img['done']
                self.Button1['command'] = self.playGame
                shutil.rmtree('./_tmp/', ignore_errors=True)
        except KeyError:
            self.insertLabelText("Impossible to get value for new versions. Try restarting the launcher or communicating support.")
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
                        self.insertLabelText(f"Downloading: {(dl/1000000):.2f}/{(total_length/1000000):.2f} Mbs, {self.TProgressbar['value']}%")
                        # self.Label1['text'] = f"Downloading: {(dl/1000000):.2f}/{(total_length/1000000):.2f} Mbs, {self.TProgressbar['value']}%"
                        novo_arquivo.write(parte)
                    download = True
        if download:
            self.insertLabelText("Waiting for updates to be installed.")
            self.descompactUpdate()
        else:
            self.insertLabelText("Communication problem with the network when checking for update.")
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
        self.insertLabelText(f"Current Version: {self.rede_dict['Version']}")
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