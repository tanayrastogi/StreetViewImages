  
# Importing the Python packages
import GSVimage

# latitude and longitude values
lat = 59.346661
lon = 18.072135

# Class Object
gsv = GSVimage.GoogleStreetViewImages(imgHeight=1080, imgWidth=1920,
                                      path_to_firefox_webdriver="/home/tanay/firefox_drivers/geckodriver")

# # Meta data
print(gsv.get_metadata(lat, lon))

# Save imgae to disk
gsv.get_image(lat, lon)

