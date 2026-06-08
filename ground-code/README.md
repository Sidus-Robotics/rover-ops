# Setup 
---
Create a venv
```
mkdir ground-code/rover-venv

cd ground-code 

python3 -m venv rover-venv/

source rover-venv/bin/activate
#Optionally you can use '.' instead of typing 'source'

# ctrl+shift+p and set this as your interpreter ground-code/rover-venv/bin/python3.10

deactivate
```
Use setuptools

https://docs.python.org/3/library/venv.html


https://setuptools.pypa.io/en/latest/userguide/quickstart.html

```
pip install --upgrade build

python -m build

pip install 

<entry>
```