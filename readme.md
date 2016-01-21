# Remedy Call Logging
### A call logging GUI application which takes a Minimum DataSet file (.xls), traverses it, displays information then using automatically fills out a call form.

This is a GUI application designed for CSC's call logging system "Remedy". This is a helper tool for employees of North Bristol Trust's IT department to log calls to our supplier easier. I have included a menu which calls our own helpdesk system "Manage Engine" (or "SDPlus") to create and update calls on the fly from the application.

Run:
```python
python remedy.py
```

or freeze the code with pyinstaller:
```python
pyinstaller remedy.spec
```