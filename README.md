# Ot Launcher Python

## Compilar usando PyInstaller:
##### Primeiro ter instalado o Python: https://www.python.org/downloads/
- #####Abrir o powershell/cmd e instalar as libs usadas:
		pip install requests
		pip install threaded
		pip install pyinstaller
- **Ainda no powershell/cmd ir até a pasta do repositorio ("ot_launcher_python-main") onde está o main.py.**

- ###### Agora ja podera compilar mas atenção a algumas configurações.
    - ###### Alterar valor das constantes em const.py
    - ###### Caso altere imagens usada em data/ e use outros nome e formatos diferente do atual devera modificar em const.py

- ##### Para compilar ira mandar o seguinte comando no powershell/cmd, sendo seus parametros ajustado como preferir.
  -  ###### Entenda os Parametros
     `--onefile` : Arquivo sera compilado totalmente em um executavel(.exe), essa opção facilita a distribuição e criar um programa mais leve, mas em meus primeiros teste o WindowsDefender acusou como mallware ([Scan - VirusTotal](https://www.virustotal.com/gui/file/39b79df18560703ceffad558cc36a6b9b3249761100c2e2a365b9df630d502ec/detection)), mas reportei esse problema enviando o launcher e eles responderam que as definições foram atualizada para corrigir isso. Caso você precise atualizar segue o procedimento que eles me [indicaram](https://www.microsoft.com/en-us/wdsi/submission/31167ef7-4e7c-49e3-bba0-8aa5a7c75111).
	 > 1 - Open command prompt as administrator and change directory to c:\Program Files\Windows Defender
	2 - Run “MpCmdRun.exe -removedefinitions -dynamicsignatures”
	3 -  Run "MpCmdRun.exe -SignatureUpdate"

     `--windowed` : Usado para interface graficas.
	 
	 `--icon="path"` : Localização do icone que sera usado no executavel.
	
	 `--name="name"` : Nome de saida do executavel.
	
	> Outros parametros que podem ser usados pode ser encontrados [aqui](https://pyinstaller.readthedocs.io/en/stable/usage.html).
	
**Comando:**

	pyinstaller --onefile --windowed --icon="data/launcher.ico" --name="perfect launcher" main.py
