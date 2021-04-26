# Reference: https://hackernoon.com/using-google-street-view-photos-as-wallpapers-a-how-to-guide-g11b3yc1


# Python Imports
import time
import requests
from selenium import webdriver
import os


class GoogleStreetViewImages:
    def __init__(self, imgHeight, imgWidth, path_to_firefox_webdriver):
        """
        INPUTS:
            imgHeight(int)  :Height of the image generated from GSV
            imgWidth(int)   :Width  of the image generated from GSV
            path_to_firefox_webdriver(str): Path to the geckodriver for firefox
            
        """

        # Google API
        self.__META_URL = "https://maps.googleapis.com/maps/api/streetview/metadata"
        self.__API_KEY = self.__get_apikey()
        self.__WEBDRIVERPATH = path_to_firefox_webdriver
        
        # Setting HTML File path
        html_filepath = os.path.join(os.path.dirname(__file__), "clean_street_view.html")
        self.__check_for_html_file(html_filepath)
        self.__HTML_PATH = 'file://{}?'.format(html_filepath)

        # Output Image folder path
        self.OUT_FOLDER_PATH = os.path.join(os.getcwd(), "generated_images/")
        # Create the folder if it does not exits
        if not os.path.exists(self.OUT_FOLDER_PATH):
            print("[GSV] Creating output folder ...", end=" ")
            os.makedirs(self.OUT_FOLDER_PATH)
            print("Done!")
        
        # Set the Selenium driver
        self.__set_webdriver(imgHeight, imgWidth)

    #######################
    ## Utility functions ##
    #######################
    def __check_for_html_file(self, filepath):
        if not os.path.isfile(filepath):
            raise Exception("The {} does not exit!".format(os.path.basename(filepath)))
        pass
    
    def __get_apikey(self, ):
        try:
            with open(".key", 'r', encoding='utf-8') as file:
                return file.read()
        except:
            raise Exception("Could not load the API Key! Check if .key file exits")

    def __set_webdriver(self, height, width):
        print("[GSV] Setting up the webdriver ...", end=" ")
        # Selenium Driver Setup
        options = webdriver.firefox.options.Options()
        options.add_argument("--log-level=3")  # minimal logging
        options.add_argument("--window-size=" + str(width) + "," + str(height))
        options.add_argument("--headless")
        self.__DRIVER = webdriver.Firefox(executable_path = self.__WEBDRIVERPATH, options=options)
        print("Done!")

    ###################################
    ## To check the GSV API response ##
    ###################################
    def _get_respone(self, lat, lon):
        locstring = str(lat) + "," + str(lon)
        return requests.get(self.__META_URL + "?key=" + self.__API_KEY + "&location=" + locstring)

    def _check_status(self, lat, lon):
        response = self._get_respone(lat, lon)
        if response.json()["status"] == "OK":
            return True
        else:
            print("[GSV]" + response.json()['error_message'])
            return False

    ###################
    ## GSV Functions ##
    ###################
    def get_metadata(self, lat, lon):
        """
        Return the meta data for the latitude and longitude from the GSV API.
        
        INPUT:
            lat(float)  :Latitude  location of the for which GSV is generated
            lon(float)  :Longitude location of the for which GSV is generated

        Return
            <dict> {lat, lon, panoID, imageDate}
            lat:        Actual latitude  of the GSV image
            lon:        Actual longitude of the GSV image
            panoID:     GSV Image ID for the image. This is also used to fetch the image.
            imageDate:  Date the image was taken in GSV.
        """
        # First check if the image is available at the location
        if self._check_status(lat, lon):
            print("[GSV] Image exits for the coordinates!")
            # Get the actual lat and lon of the image from the METADATA
            print("\n[GSV] Generating MetaData ...", end=" ")
            response = self._get_respone(lat, lon)
            metaData = {"lat": response.json()["location"]["lat"],
                        "lon": response.json()["location"]["lng"],
                        "panoID": response.json()["pano_id"],
                        "imageDate": response.json()["date"]}
            print("Done!")
            return metaData
            
        else:
            return None
        
    ########################
    ## Image from  GSV ##
    ########################
    def get_image(self, lat, lon):
        """
        Function saved the the image for the latitude and logitude to "~/generated_images/".
        
        INPUT:
            lat(float)  :Latitude  location of the for which GSV is generated
            lon(float)  :Longitude location of the for which GSV is generated
        """
        # First check if the image is available at the location
        if self._check_status(lat, lon):
            print("[GSV] Image exits for the coordinates!")
            # Generate Image for the lat lon
            print("[GSV] Generating Image ..", end = " ")
            html_address = self.__HTML_PATH + "lat={}&lng={}".format(lat, lon)
            self.__DRIVER.get(html_address)
            time.sleep(1.0)  # wait for image to load

            # Save image with PanoID
            image_path = os.path.join(self.OUT_FOLDER_PATH, str(self.get_metadata(lat, lon)["panoID"]) + ".png")
            self.__DRIVER.save_screenshot(image_path)
            print("Done!")
            
        else:
            return None

if __name__ == "__main__":
    pass


