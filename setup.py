from cx_Freeze import setup, Executable
import sys,pkgutil,os

Import=['sys', 'os','urllib','logging','requests','numpy','threading','PyQt5','idna','xml','urllib3','http','email','charset_normalizer','json','certifi']
BasicPackages=['collections','encodings','importlib'] + Import

name = 'BlingERP-Python'
version = '1.0.0'
author = 'José Henrique S.S'

def AllPackage():
    return [i.name for i in list(pkgutil.iter_modules()) if i.ispkg]
def notFound(A,v):
    try: A.index(v); return False
    except: return True

base = None
if sys.platform == 'win32':
    base = "Win32GUI"

build_exe_options = {
    "includes":['queue','secrets'],
    "include_files":[r"UI's"],
    "zip_include_packages": BasicPackages,
    "excludes": [i for i in AllPackage() if notFound(BasicPackages,i)],
    "optimize": 1,
}

bdist_msi_options = {
    'add_to_path': False,
    'initial_target_dir': os.environ['ALLUSERSPROFILE']+f'\{name}',
    'target_name': name,
}

mainexe = Executable("main.py",
base=base,
shortcut_name=name,
shortcut_dir="DesktopFolder",
copyright="Copyright (C) 2022 José Henrique S.S")

setup(
    name=name,
    version=version,
    author=author,
    options = {"build_exe": build_exe_options,
    'bdist_msi': bdist_msi_options},
    executables=[mainexe]
)