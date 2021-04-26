# StreetViewImages
Module for downloading high-resolution Google Street View images given (lat, lng) using Google Street View Service. 


### Usage
The module assumes that, 
- Selenium with Python is already setup with Firefox and Gecko-webdriver.
- API key from Google Cloud to access the Street View API is stored in file called *.key*.

The package give information about the METADATA data about the GSV for the lat/lon and can get the image from the GSV.
METADATA for each lat/lon, 
- LAT: Actual latitude of the GSV image.
- LON: Actual longitude of the GSV image.
- PANOID: Google Service ID for each iamge. 
- IMAGEDATE: Month-Year when image is taken by Google. 

Check **example.py** on how to use. 

### Webdriver for Selenium
- One will need the webriver for the browser that will be used to open the broweser from python and run the HTML script. 
- The scrip uses **FIREFOX** webdriver to run. 


**REFERENCES**
- [Hackernoon Article](https://hackernoon.com/using-google-street-view-photos-as-wallpapers-a-how-to-guide-g11b3yc1)
- [Google Street View Service](https://developers.google.com/maps/documentation/javascript/streetview)
- [Setting up Selenium with Python](https://trendoceans.com/how-to-install-and-setup-selenium-with-firefox-on-ubuntu/)
- [Installing Selenium](https://selenium-python.readthedocs.io/installation.html) 
- [Firefox Gecko-webdriver](https://github.com/mozilla/geckodriver/releases/tag/v0.29.1) 
