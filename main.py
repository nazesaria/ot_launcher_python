from tkinter import *
import sys
import tkinter.ttk as ttk
import json
import os
import requests

import pymysql.cursors
# https://github.com/nazesaria/ot_launcher_python/archive/main.zip
# Execução do Launcher
class Launcher:

    local_dict = {}
    rede_dict = {}
    progress = 100
    buttons = ["Check", "Update", "Done!"]
    buttons_img = {'check': '', 'update': '', 'done': ''}

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

        self.Label1 = Label(root, text='Update Version: {}'.format(self.local_dict['Version']), background="#673434")
        self.Label1.place(relx=0.025, rely=0.88, height=18, width=200)
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
            with open('_tmp/{}'.format(endereco), 'wb') as novo_arquivo:
                for parte in resposta.iter_content(chunk_size=256):
                    novo_arquivo.write(parte)
            print("Download finalizado. Arquivo salvo em: {}".format(endereco))
        else:
            resposta.raise_for_status()

    def makeRedeDict(self):
        self.downloadArchive('https://raw.githubusercontent.com/nazesaria/ot_launcher_python/main/main.py')

    def checkUpdate(self):
        self.makeRedeDict()
        # new_version = 1.002
        # if new_version > self.local_dict['Version']:
        #     self.Button1['image'] = self.buttons_img['update']
        # else:
        #     self.Button1['image'] = self.buttons_img['done']

    def loadFromJson(self, file):
        with open(file, 'r') as archive:
            txt = archive.read()
            return json.loads(txt)

    def writeDictFromJson(self, file):
        with open(file, 'w') as arquivo:
            arquivo.write(json.dumps(self.local_dict, indent=2))

    def progressBarValue():
        pass

launcher = Launcher()