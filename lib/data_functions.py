import csv
from zipfile import ZipFile
from requests import get
from io import BytesIO

def fda_reg(path):
    """
    Point this function towards the fdaaa_regulatory_snapshot.csv file to turn it into a
    dictionary for what you need in this analysis
    See https://doi.org/10.1101/266452 for more information
    """
    fda_reg_dict = {}
    with open(path) as old_fda_reg:
        reader = csv.DictReader(old_fda_reg)
        for d in reader:
            fda_reg_dict[d['nct_id']] = d['is_fda_regulated']
    return fda_reg_dict

def get_data(path, file, zipped=False):
    """
    Quick function to load the raw ClinicalTrials.gov data which is a CSV of JSON (can think of as ndjson as well)
    """
    if zipped:
        #For now, lets just work with the local case
        #This assumes a zipped csv file
        #with ZipFile(BytesIO(get(path, stream=True).content), 'r') as zf:
        with ZipFile(path + '/' + file, 'r') as zf:
            #this sting manipulation probably isn't sustainable outside of my useage.
            with zf.open(file.replace('.zip',''), 'r') as ctgov:
                lines = ctgov.readlines()
                return lines

    else:
        with open(path + '/' + file, 'r') as ctgov:
            lines = ctgov.readlines()
            return lines
    
        
