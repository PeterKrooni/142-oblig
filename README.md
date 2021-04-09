### INF142 Mandatory Assignment
    Group 26 
    Jørgen Lohne, Petter Tobias Madsen and Peter Krooni
---
# FMI Weather Station Storage Interaction System 

Main entry point of application is FMI.py
There are two versions of the program available, CLI (command line interface) and Web (web browser based, using flask).


### How to run:
1. Clone repository
2. Install packages in requirements.txt (this can be done automatically when cloning the project into an IDE such as Pycharm)
3. Run FMI.py and follow the instructions in the console

If you are running the web version of the program, and the browser window doesn't automatically open on running, open your browser of choice and enter http://localhost:5000

Data entries received from the weather station is written to 'storage.txt'.

### Extras
As well as completing the MVP we decided to add a webserver using flask. In addtion we have created a web-GUI for the web-server, here you are able to see two charts of the data, one displays data from the  72 last hours, and one for all-time. To use these extra features, use the web command when prompted while running FMI.py
