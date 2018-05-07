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
  
  The package works by:
- Pulling the git file
- Going into one of the folders for which type of metadata you would like to view, 
- Editing the harest file to point to the desired repository,
- Running harvest.py,
- Then running flare.py 
- And finally viewing the data set by opening on of the .html files in a 
web browser.

For more detailed step-by-step instructions visit our website:
(Instructions comming soon) https://glamviz.commons.gc.cuny.edu/

# Getting Started

The GLAM Project supports configuration of repository labels and urls to harvest data into sets and tranform data for data visualization.

## Installation
### Prerequisites

* git: https://git-scm.com/downloads
* Python 3: https://www.python.org/downloads/

> Windows now has a bonafide package manager:
> * Chocolatey: https://chocolatey.org/install
>```bash
>C:\> choco install git
>C:\> choco install python 
>```



### Procedure

* from a command prompt (any directory), install virtualenv using Python's pip tool:
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
* Load virtual environment in a subdirectory, such as venv
```
virtualenv venv
```

- Activate the virtual environment (it will say venv infront of the directory location on the command prompt, that is how you know you are in the virtual environment)
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
* Load the Swagger forms for data processing:

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
- click GET /harvest/ListSets and Try it out! to verify data is available.
- click GET /harvest/WriteAllRecords and Try it out! to start harvesting.
> Harvesting may take a long time to complete. Leave the form alone while
> the progress indicator on the form is still moving.  A list of the sets
> processed with be returned when it's finished.
- click GET /harvest/WriteAllSetsFile to create the consolidate 'all_sets.json'
file that is used in tranformations.
- click *Show/Hide* at top of *harvest* section to close it

## Transform Data

- click on *transform* to open its options
- click GET /transform/FlareRecords
- set subject_count_min (choose 3) and subject_count_max (choose 100) values
- click Try it out!
- note the *filepath* returned

## Show Visualization

- open Treemap.html within your browser

```
example:
file:///C:/Users/Username/ProjectsDirectory/GlamViz/Treemap.html
```

- Browse to the transformed data directory, it will be the same as listed on the filepath from the transformation API output

