# GSFScraper

GSFScraper is a simple scraper that helps find garage sales in the US.

## Installation

Requirements:
- Python 3.10
- [Mozilla Gecko Driver](https://github.com/mozilla/geckodriver/releases)

**Procedure:**
- Download and extract the [latest release](https://github.com/Math-Morin/GSFScraper/releases) of the source code.
- In the project folder, run ```pip install -r requirements.txt```. This will install all dependencies globally.
- The app can now be launched.

**If you do not want to install the dependencies globally, here is an alternative procedure using a virtual environment:**
- Download and extract the [latest release](https://github.com/Math-Morin/GSFScraper/releases) of the source code.
- In the project folder, run ```pipenv install```. This will install all dependencies in a virtual environment.
- Set the virtual environment with ```pipenv shell```. This must be done each time before launching the app.
- The app can now be launched.

## Execution
*Note: if using a virtual environment, you must run* ```pipenv shell``` *from inside the project folder before launching the app.*

### Interactive mode
Without any argument, i.e. ```python GSFScraper.py``` the app launches in interactive mode. Prompts will ask you to choose between 'single location' and 'multiple locations from list'.
Then, simply enter either the location or the name of the file containing the list of locations.

### Arguments
```GSFScraper.py [ -h ] [ -s CITY STATE | -l FILE_NAME ]```

To facilitate automation, arguments can be passed to the app.

Run ```python GSFScraper.py -h``` for help with arguments.

#### Single location
With either ```-s``` or ```--single``` given as an argument, the app will directly scrape for the given location.

*Note: location with spaces in them must be surrounded with double quotation marks.*

Examples: 
- ```python GSFScraper.py -s "new york" "new york"```
- ```python GSFScraper.py --single "los angeles" california```

#### Multiple locations from file
With either ```-l``` or ```--list``` given as an argument, the app will directly scrape for the given locations listed in the given file.

Examples: 
- ```python GSFScraper.py -l example.txt```
- ```python GSFScraper.py --list example.txt```

## Locations list file
A text file listing locations can be added to the 'input' folder which is located in the project folder.
The format of the list must be one location per line, with each location described by the name of the city and its state, separated by a comma : ```city , state```

The app will scrape for each location. If a line does not respect this format, it will be ignored and a log entry will be added to let you know.

Comments can be added to this file. Eveything after a '#' character will be ignored.

The following is the content of example.txt located in the 'input' folder by default:
```
# All lines beginning with a '#' character are comments that will be ignored when reading the list.
# A comma ',' is used as a separator between the city name and the state. All lines must contain one and only one ',' character. Otherwise, they will be ignored.

# Major cities
new york, new york # comments can also be added at the end of a line
los angeles, california
seattle, washington
detroit, michigan

# Minor cities
Boulder, Colorado
Waterbury, Vermont
```
## Output
Each scraping session will output files in a uniquely named folder in the 'output' folder. This unique name is the date and time of the execution. If a list of locations are scraped, all files (one per location) will be created in the same folder.

A log file can also be found in this folder, describing the session events and errors.

## Configuration
The config.json file contains the few configurations available for the app. Here is an example of its content:
```
{
    "load time allowed": 5,
    "output to csv": "false",
    "output to excel": "true",
    "output to json": "false"
}
```

- ```load time allowed``` : Time in seconds allowed to the page to load before fetching info. Increase this if load time is insufficient.
- ```output to csv``` : Whether or not to output the data to a .csv file
- ```output to excel``` : Whether or not to output the data to a .xlsx file
- ```output to json``` : Whether or not to output the data to a .json file

*Note : if this file is deleted, a new one will be created with default values to 5 seconds and all output file types to true.*
