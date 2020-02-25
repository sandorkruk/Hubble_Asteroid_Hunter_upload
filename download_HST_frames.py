'''
    Downloads HST jpeg frames and produces 4 equal cutouts for the Asteroid Hunter Project
'''

from PIL import Image
import os
import numpy as np
from urllib.request import urlretrieve
from urllib.error import HTTPError
import pandas as pd

#4-side equal cutouts

def crop(im,height,width):
    # im = Image.open(infile)
    imgwidth, imgheight = im.size
    for i in range(np.int(imgheight//height)):
        for j in range(np.int(imgwidth//width)):
            # print (i,j)
            box = (j*width, i*height, (j+1)*width, (i+1)*height)
            yield im.crop(box)



if __name__ == '__main__':

	data = pd.read_csv('ACS_remaining_blind_images.csv')

	numb_obs_ids = len(data)
	progress_counter = 0
	#%timeit

	cutout_metadata = pd.DataFrame()

	for i in range(0,len(data)):
	    progress_counter += 1
	    #if progress_counter % 100 == 0:
	    print(progress_counter, '/', numb_obs_ids)
	    #donwloand URL
	    print("http://hst.esac.esa.int/ehst-sl-server/servlet/data-action?RETRIEVAL_TYPE=PRODUCT&ARTIFACT_ID="+str(data["observation_id"][i])+"_drc.jpg")
	    try:
	    	x=0
	    	urlretrieve("http://hst.esac.esa.int/ehst-sl-server/servlet/data-action?RETRIEVAL_TYPE=PRODUCT&ARTIFACT_ID="+str(data["observation_id"][i])+"_drc.jpg", "cutout_drc/"+str(data["observation_id"][i])+".jpg")
	    except HTTPError:
	        x=1
	        urlretrieve("http://hst.esac.esa.int/ehst-sl-server/servlet/data-action?RETRIEVAL_TYPE=POSTCARD&OBSERVATION_ID="+str(data["observation_id"][i]), "cutout_drc/"+str(data["observation_id"][i])+".jpg")
	    #split image into 4
	    im = Image.open("cutout_drc/"+str(data["observation_id"][i])+".jpg")
	    imgwidth, imgheight = im.size
	    height = np.int(imgheight/2)
	    width =  np.int(imgwidth/2)
	    start_num = 0
	    for k,piece in enumerate(crop(im,height,width),start_num):
	        img=Image.new('L', (width,height), 255)
	        img.paste(piece)
	        img = img.resize((np.int(img.size[0]/2),np.int(img.size[1]/2)),Image.ANTIALIAS)              
	        path = os.path.join("cutout_unique/"+str(data["observation_id"][i])+"_%d.jpg" % (int(k+1)))
	        img.save(path,optimize=True,quality=100)

	        keywords_copy = {}
	        keywords_copy['!filename'] = str(data["observation_id"][i])+"_%d.jpg" % (int(k+1))
	        keywords_copy['!observation_id'] = data["observation_id"][i]
	        keywords_copy['#algorithm'] = data["algorithm_name"][i]
	        keywords_copy['!collection'] = data["collection"][i]
	        keywords_copy['#end_time'] = data["end_time"][i]
	        keywords_copy['#end_time_mjd'] = data["end_time_mjd"][i]
	        keywords_copy['#total_exposure_duration'] = data["exposure_duration"][i]
	        keywords_copy['#instrument_configuration'] = data["instrument_configuration"][i]
	        keywords_copy['!instrument_name'] = data["instrument_name"][i]
	        keywords_copy['!RA'] = data['ra'][i]
	        keywords_copy['!Dec'] = data['dec'][i]
	        keywords_copy['#members'] = data["members"][i]
	        keywords_copy['#members_number'] = data["members_number"][i]
	        keywords_copy['#observation_uuid'] = data["observation_uuid"][i]
	        keywords_copy['#observation_type'] = data["obs_type"][i]
	        keywords_copy['#pi_name'] = data["pi_name"][i]
	        keywords_copy['#proposal_id'] = data["proposal_id"][i]
	        keywords_copy['#release_date'] = data["release_date"][i]
	        keywords_copy['#run_id'] = data["run_id"][i]
	        keywords_copy['#set_id'] = data["set_id"][i]
	        keywords_copy['!start_time'] = data["start_time"][i]
	        keywords_copy['#start_time_mjd'] = data["start_time_mjd"][i]
	        keywords_copy['#target_description'] = data["target_description"][i]
	        keywords_copy['!target_name'] = data["target_name"][i]
	        keywords_copy['#size_original_w'] = imgwidth
	        keywords_copy['#size_original_h'] = imgheight
	        keywords_copy['#size_cutout_w'] = (np.int(img.size[0]/2))
	        keywords_copy['#size_cutout_h'] = np.int(img.size[1]/2)
	        keywords_copy['ESASky'] = "[Link to ESA Sky](+tab+http://sky.esa.int/?target=" + str(data["ra"][i]) + "%20" + str(data["dec"][i]) +"&hips=HST+ACS&fov=0.1&cooframe=J2000&sci=true&lang=en)"
	        keywords_copy['ESA Archives'] = "[Link to ESA Archives](+tab+http://hst.esac.esa.int/ehst/#observationid="+str(data["observation_id"][i])+")"
	        if x==0:
	            keywords_copy['!exposure']="drc"
	            keywords_copy['#Full frame'] = "[Link to ESA Archives](+tab+http://hst.esac.esa.int/ehst-sl-server/servlet/data-action?RETRIEVAL_TYPE=PRODUCT&ARTIFACT_ID="+str(data["observation_id"][i])+"_drc.jpg)"
	        else:
	            keywords_copy['!exposure'] = "drz"
	            keywords_copy['#Full frame'] = "[Link to ESA Archives](+tab+http://hst.esac.esa.int/ehst-sl-server/servlet/data-action?RETRIEVAL_TYPE=POSTCARD&OBSERVATION_ID=" + str(data["observation_id"][i])+")"
	        cutout_meta = pd.DataFrame(data=keywords_copy, index=[data["observation_id"][i]])
	        cutout_metadata = cutout_metadata.append(cutout_meta)

	cutout_metadata.to_csv('cutout_unique/metadata.csv', index=False)


