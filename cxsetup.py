import cx_Freeze as cx

cx.setup(
name='SisPAF',
version='1.0',
author='Luis Erik y Esteban',
author_email='luis_enrique270@outlook.com',
description='Sistema para la predicción de la Actividad Farmacológica',
url="http://sispaf-example.com",
packages=['/home/henryp/Desktop/pruebafreeze'],
executables=[
cx.Executable('Principal.py',
targetName='SisPAF', icon='/home/henryp/Desktop/School/TT2/TT2_032/Logotipo/Individuales/molecula.ico')],
options={
'build_exe': {
'packages': ['numpy', 'tkinter', 'requests', 'PIL', 'selenium', 'Bio', 'pubchempy', 'pypdb', 'ratelimit', 'pandas', 'sklearn'],
'includes': ['numpy.core._methods', 'numpy.lib.format']}
})