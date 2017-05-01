# Remedy Call Logging
### A call logging GUI application which takes a Minimum DataSet file (.xls), traverses it, displays information then using automatically fills out a browser form for submission.

This is a GUI application designed for CSC's call logging system "Remedy". This is a helper tool for employees of North Bristol Trust's IT department to log calls to their supplier ("CSC") easier. I have included a menu which calls our own helpdesk system "ManageEngine" (or "SDPlus") to create and update calls on the fly from the application utilising the ManageEngine Rest API.

Run:
```python
python remedy.py
```

or freeze the code with pyinstaller:
```python
pyinstaller remedy.spec
```

see [Remedy Documentation](Remedy Documentation.txt) for more details.