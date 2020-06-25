#! /bin/bash
echo ----------- Instalando Python3.6 --------------
sudo apt install python3.6.9
echo -------------- Verificando la versión de pip --------------
pip3 --version
echo -------------- Instalando Tkinter --------------
sudo apt-get install python3-tk
echo -------------- Instalación de Requests --------------
pip3 install requests
echo -------------- Instalación de Selenium --------------
pip3 install selenium
echo -------------- Instalando Pillow-PILImage
pip3 install Pillow
echo -------------- ChromeDriver --------------
sudo apt-get update 
sudo apt-get install -y unzip xvfb libxi6 libgconf-2-4
echo -------------- Instalar Chrome --------------
echo agregando el repositorio de Google Chrome en nuestro sistema
wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | sudo apt-key add -
sudo sh -c 'echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list'
sudo apt-get
sudo apt-get install google-chrome-stable
echo ------------- Instalando Chromedriver ----------------
wget https://chromedriver.storage.googleapis.com/83.0.4103.39/chromedriver_linux64.zip
unzip chromedriver_linux64.zip
sudo mv chromedriver /usr/bin/chromedriver
sudo chown root:root /usr/bin/chromedriver
sudo chmod +x /usr/bin/chromedriver
echo ------------- Instalando BioPython ----------------
pip3 install biopython
echo ------------- Instalando PubChem -----------------
pip3 install PubChemPy
echo ------------- Instalando Pypdb -------------------
pip3 install pypdb
echo ------------ Instalando Matplotlib ----------------
pip3 install matplotlib
echo ------------ Ratelimit -------------------------
pip3 install ratelimit
echo ------------- Instalando mgltools ------------------
wget http://mgltools.scripps.edu/downloads/downloads/tars/releases/REL1.5.6/mgltools_x86_64Linux2_1.5.6.tar.gz
tar -xzvf mgltools_x86_64Linux2_1.5.6.tar.gz
cd mgltools_x86_64Linux2_1.5.6
./install.sh
cd MGLToolsPckgs/AutoDockTools/Utilities24
sudo cp prepare_ligand4.py /usr/local/bin
sudo cp prepare_receptor4.py /usr/local/bin
sudo cp prepare_gpf4.py /usr/local/bin
cd ../../..
cd bin
sudo cp pythonsh /usr/local/bin
echo ------------ Instalando AutoDock-Vina -------------
sudo wget http://vina.scripps.edu/download/autodock_vina_1_1_2_linux_x86.tgz
echo descomprimir
tar -xzvf autodock_vina_1_1_2_linux_x86.tgz
cd autodock_vina_1_1_2_linux_x86/bin
cp vina /usr/local/bin
echo -------------- Instalando Autogrid ----------------
sudo wget http://autodock.scripps.edu/downloads/autodock-registration/tars/dist426/autodocksuite-4.2.6-x86_64Linux3.tar
echo Descomprimiendo autodocksuite
tar -xvf autodocksuite-4.2.6-x86_64Linux3.tar
cd x86_64Linux3
cp autodock4 /usr/local/bin
cp autogrid4 /usr/local/bin
echo -------------- Instalando Pandas -----------------
pip pip3 install pandas
echo -------------- Instalando Scikit-learn -----------
pip3 install scikit-learn
echo -------------- Instalando NumPy -----------
pip3 install numpy
echo Finish 
exit
