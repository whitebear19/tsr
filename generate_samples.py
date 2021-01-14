#!/usr/bin/env python
#generate_samples.py

""" Generates and downloads new samples of protein PDB IDs.
	Generates new samples of protein PDB IDs from RCSB proteins 
	website and downloads the PDB files to a local directory.
	Attributes:
		path: Directory where the downloaded PDB files are stored.
		
"""


import os, time
import requests
import urllib.request
import pandas as pd

__author__ = "Venkata Sarika Kondra"

__version__ = "1.0.1"
__maintainer__ = "Venkata Sarika Kondra"
__email__ = "c00219805@louisiana.edu"


def generate_samples(directory_path, msg = ''):
	"""Generate samples from a given sample_details file."""

	non_functional_urls = []
	start = time.time()

	#arr = ['1h7w', '1jmx', '1rq6', '2j9u', '1d9c', '2ciw']
	samples_file = pd.read_csv(os.path.join(directory_path,
										 'sample_details.csv'))

	sample = samples_file['protein'].map(str).values
	for id in sample: 
			#Generate the downloadable URL
			url = "http://files.rcsb.org/download/{}.pdb".format(id.replace(
					'+', ''))
			#Check if the URL exists, otherwise skip that PDB ID
			request = requests.get(url)
			if request.status_code == 200:
				outputFilename = "{}//{}.pdb".format(directory_path,str(id.replace('+', '')))
				response = urllib.request.urlopen(url)
				zippedData = response.read()
				# save data to disk
				output = open(outputFilename,'wb')
				
				output.write(zippedData)
				output.close()
				print(url , " extracted to ",outputFilename)
			else:
				non_functional_urls.append(id)
				continue
	if non_functional_urls:
		msg = "Un available URLs- {}".format(non_functional_urls)
		print(msg)
	# msg = msg + '\n' + 'Downloaded {}/{} PDB files for ''{}'' and saved at {}'.format(
	# 		len(sample) - len(non_functional_urls), len(sample), 
	# 		sample_name, os.path.join(directory_path, sample_name))
	msg = msg + '\n' + 'Time taken for generating sample is {} mins.'.format(
            round((time.time()-start)/60, 2))
												
	print(msg)
	return msg

generate_samples('D:/Daily-Work/2021/1/TSR/Main')