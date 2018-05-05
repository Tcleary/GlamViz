# Glam Out-of-the-Box Visualizations
This is an OAI-PMH visualization tool for Gallery, Library, Archive and Museum repositories and websites. It pulls metadata out of of a systems OAI-PMH API and then reformats it to let you create a graph of what subjects, locations, or material types are in the collection.  The graphs are created by using interactice D3 javacript templates from D3.js

## Instructions
  We’ve aimed to create an easy to use package to harvest and transform metadata from repositories that can be used with a few stock visualizations that wekvenfound and edited. The package works by:
-Pulling the git file
-Going into one of the folders for which type of metadata you would like to view, 
-Editing the harest file to point to the desired repository,
-Running harvest.py,
-Then running flare.py 
-And finally viewing the data set by opening on of the .html files in a webrowser.

For more detailed step-by-step instructions visit our website: (Instructions comming soon) https://glamviz.commons.gc.cuny.edu/

# Getting Started

The GLAM Project supports configuration of repository labels and urls to harvest data into sets and tranform data for data visualization.

## Installation

### Prerequisites

* Python 3: https://www.python.org/downloads/
* virtualenv: https://virtualenv.pypa.io/en/stable/installation/


### Procedure

* from within a directory for projects, clone the GlamViz repository:
```
git clone git clone https://github.com/Tcleary/GlamViz.git
```
* change into the cloned directory:
```
cd GlamViz/GLAM
```
* Load virtual environment

Windows:
```
.\venv\Scripts\activate\
```
Mac:
```
.\venv\bin\actovate
```
Run the GLAM app:
```
python GLAM.py
```
Load the Swagger forms for data processing:
http://127.0.0.1:5000/



