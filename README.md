# Hubble_Asteroid_Hunter_upload
Creating images and uploading to the Zooniverse Hubble Asteroid Hunter project

This script was used to create the images and metadata to be uploaded to www.asteroidhunter.org.

It requires a table from eHST TAP with the observations. Currently obtained with the following ADSQL code:

SELECT * FROM ehst.observation WHERE collection='HST'AND obs_type='HST Composite'AND instrument_name='ACS/WFC' AND exposure_duration>0

The script downloads the corresponding HST frame (drz or drc .png file from eHST) and splits it into 4 equal quadrants to be uploaded to asteroidhunter.org
