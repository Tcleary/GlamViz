# Glam Out-of-the-Box Visualizations
This is an OAI-PMH visualization tool for Gallery, Library, Archive and Museum
repositories and websites. It pulls metadata out of of a systems OAI-PMH API 
and then reformats it to let you create a graph of what subjects, locations, 
or material types are in the collection.  The graphs are created by using 
interactice D3 javacript templates from D3.js

## Instructions
  We’ve aimed to create an easy to use package to harvest and transform
  metadata from repositories that can be used with a few stock visualizations
  that we have found and edited.
  
  This page will show you how to
  - Pull the git file
  - Set up your Python enviroment
  - Use our GUI interface to harvest and transform the data
  - And finally viewing the data as a Treemap.

For more detailed step-by-step instructions visit our website:
(Instructions comming soon) https://glamviz.commons.gc.cuny.edu/

# Getting Started

The GLAM Project supports configuration of repository labels and urls to harvest data into sets and tranform data for data visualization.

## Installation
### Prerequisites

* git: https://git-scm.com/downloads
* Python 3: https://www.python.org/downloads/

> Note: Windows now has a bonafide package manager called Chocolatey. We used this to help create our project.
> * Chocolatey: https://chocolatey.org/install
>```bash
>C:\> choco install git
>C:\> choco install python 
>```



### Procedure

* Open your command prompt and install virtualenv (a Python virtual enviroment package) using Python's pip tool:
```
pip install virtualenv
```
* from within a directory for projects, clone the GlamViz repository:
```
git clone https://github.com/Tcleary/GlamViz.git
```
* change into the cloned directory:
```
cd GlamViz
```
* Create and load virtual environment in a subdirectory, for example we created one called "venv"
```
virtualenv venv
```
* Activate the virtual environment (it will say venv infront of the directory location on the command prompt, that is how you know you are in the virtual environment)
```
venv\Scripts\activate
```
* install the required python libraries listed in the requirements.txt file
```
pip install -r requirements.txt
```
* Run the GLAM app:
```
python glamviz/app.py
```
* Load the Swagger forms for data processing
Your script will run and end on 
```
Running on http:127.0.0.1:5000
```
This means your enviroment is running and accessible through your local host. Leave your command prompt open and then go to this link in a web browser:

http://127.0.0.1:5000/

## Configure OAI Repository

From the Glamviz swagger form:

- click on *admin* to open up the section options
- click GET /admin/Repository and notice it's not configured yet
- click POST /admin/Repository and paste in a repository configuation:
```json
{
  "label": "Laguardia",
  "url": "http://archives.laguardia.edu/oai2"
}
```   
- click *Try it out!* to submit the form for configuration
- click GET /admin/Repository then click its *Try it out!* button
to verify the repository is set.
- click *Show/Hide* at top of *admin* section to close it

## Harvest Data

- click on *harvest* to open its section options
- click GET /harvest/ListSets and *Try it out!* to verify data is available.
- click GET /harvest/WriteAllRecords and *Try it out!* to start harvesting.
> Harvesting may take a long time to complete. Leave the form alone while
> the progress indicator on the form is still moving.  A list of the sets
> processed with be returned when it's finished.
- click GET /harvest/WriteAllSetsFile to create the consolidate 'all_sets.json'
file that is used in tranformations.
- click *Show/Hide* at top of *harvest* section to close it

## Transform Data

- click on *transform* to open its options
- click GET /transform/FlareRecords
- set subject_count_min and subject_count_max values, (this sets a limit on what subjects appear, making it possible to view all subjects only appearing one, twice, or only subjects that appear between 50 to 100 times, etc.)
- click Try it out!
- note the *filepath* returned, copy this to use later when creating the visualization

## Show Visualization

-Navigate in your file directory (My Computer) to where you installed the GlamViz folder, if you specified a different folder, it will be found there.
```
example:
C:/Users/YOURUSERNAME/GlamViz
```
- Double click to open Treemap.html within your browser
- Once the page is open in your browser, click the "Browse" button
- In the browse window, navigate to the transformed data directory using the filepath from the transformation API output
```
example:
C://Users/YOURUSERNAME/GlamViz/instance/data/transformed/LableFromPostBox/all_sets_min_1_max_100.json
```
-Once opened a Treemap D3 node.js visualization will be generated

