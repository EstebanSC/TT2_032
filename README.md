# Sistema para la Predicción de la Actividad Farmacológica SisPAF.
# Desarrollado por: Luis Enrique Garcia Peregrino, Esteban Sánchez Cuevas y Adolfo Erik Morales Castellanos

![SisPAF](https://github.com/EstebanSC/TT2_032/blob/master/Logotipo/Logotipo.png?raw=true)

SisPAF es un sistema de información que hace uso de la metodología QSAR y la regresión lineal para predecir la efectividad de un fármaco sobre las proteínas de una patología.

Surge como un prototipo de solución para el proceso de experimentación en la industria farmacológica, asistiendo en el desarrollo de nuevos fármacos o en la mejora de los ya existentes.

Supone una alternativa al método tradicional de la experimentación, el cual se basa en un proceso muy largo y costoso de recopilación de fármacos candidatos, realización de pruebas en animales o tejidos vivos y generación de resultados. Este proceso llega a durar hasta 5 años y es muy difícil de replicar. Para ello SisPAF puede asistir a los investigadores encargados de realizar la tarea previamente descrita en el proceso de recopilación y selección de fármacos candidatos indicando cuales de los fármacos pueden tener un buen resultado y cuales no deberían incluirse en el estudio.


#Instalación.

SisPAF se encuentra disponible unicamente para distribuciones de Linux basadas en debian.

Al descargar el proyecto, se le dan permisos de ejecución al archivo Instalacion.sh y se ejecuta en la misma terminal.

Dar permisos de instalación al archivo estando en el directorio donde se descargo SisPAF:

```shell
sudo chmod +x Instalacion.sh
```

Para ejecutar SisPAF se ingresa el siguente comando en la terminal:

```shell
python3 Principal.py
```

En el directorio donde se descargó el proyecto se puede encontrar un archivo de ejemplo con el nombre  ConjuntoI_p.txt el cual es un ejemplo del formato que SIsPAF requiere para trabajar. En este archivo se deben enlistar los fármacos y las proteínas sobre las que se desea los fármacos actuen.

------------------------------------------------------------------------------------------------------------------------------------------------------------------

# System for Predicting Pharmacological Activity.
# Developed by: Henry, Steve and Erik

SisPAF is an information system that makes use of the QSAR methodology and linear regression to predict the effectiveness of a drug on the proteins of a pathology.

It emerges as a prototype solution for the experimentation process in the pharmacological industry, assisting in the development of new drugs or in the improvement of existing ones.

It is an alternative to the traditional method of experimentation, which is based on a very long and expensive process of collecting candidate drugs, conducting tests on animals or living tissues and generating results. This process lasts up to 5 years and is very difficult to replicate. For this, SisPAF can assist the researchers responsible for carrying out the task previously described in the process of compilation and selection of candidate drugs, indicating which of the drugs may have a good result and which should not be included in the study.

# Installation.

SisPAF is available only for debian-based Linux distributions.

When downloading the project, execute permissions are given to the Instalacion.sh file and it is executed in the same terminal.

Give installation permissions to the file being in the directory where SisPAF was downloaded:

```shell
sudo chmod +x Instalacion.sh
```

To run SisPAF, enter the following command in the terminal:

```shell
python3 Principal.py
```

In the directory where the project was downloaded you can find an example file with the name ConjuntoI_p.txt which is an example of the format that SIsPAF requires to work. In this file you must list the drugs and the proteins on which you want the drugs to act.
