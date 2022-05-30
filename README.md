
# gudlift-registration
An application where users can book or reserve a place in strength competitions for the company Güdlft.

1. Objectives
	- Find the bugs
	- Correction of bugs
	- Implementation of new functionalities
	- Create a branch for each bug correction, improvement or new functionality created
	- Test the application using pytest or unittest and its performance with locust


2. Getting Started

    This project uses the following technologies:

    * Python v3.x+
    * [Flask](https://flask.palletsprojects.com/en/1.1.x/)
    * [Pytest](https://pypi.org/project/pytest/)
    * [Virtual environment](https://virtualenv.pypa.io/en/stable/installation.html)

        This ensures you'll be able to install the correct packages without interfering with Python on your machine.

        Before you begin, please ensure you have this installed globally. 


3. Installation

    - After cloning, change into the directory and type <code>virtualenv .</code>. This will then set up a a virtual python environment within that directory.

    - Activate the virtual environment with <code>source bin/activate</code>. You should see that your command prompt has changed to the name of the folder. This means that you can install packages in here without affecting affecting files outside. To deactivate, type <code>deactivate</code>

    - Install packages with <code>pip install -r requirements.txt</code>. This will install all the packages listed in the respective file.

    - Set an environmental variable to the python file with `export FLASK_APP=server.py` Check [here](https://flask.palletsprojects.com/en/1.1.x/quickstart/#a-minimal-application) for more details

    - To run the application type either <code>flask run</code> or <code>python -m flask run</code>. The app should respond with an address you should be able to go to using your browser.

4. Current Setup

    The app is powered by [JSON files](https://www.tutorialspoint.com/json/json_quick_guide.htm). This is to get around having a DB until we actually need one. This are:
     
    * competitions.json - list of competitions
    * clubs.json - list of clubs with relevant information. You can look here to see what email addresses the app will accept for login.

5. Tests

    Testing the application with unit test and integration test with pytest and to check if the test has been passed:
    
    * run `pytest tests/unit_test` for unit test and
    * run `pytest tests/integration_test` for test integration
