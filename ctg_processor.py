from datetime import date, datetime
from time import time
import os
from zipfile import ZipFile
import gc

from tqdm.auto import tqdm

from lib.data_functions import get_data, fda_reg

#Tests to consider
#Is the data well formatted?
#Maybe we should force a date to be in the file name?

#For as long as I'm the primary person using this, we can assume the structure of the file names a build off of that.
#That is either:
#clinicaltrials_raw_clincialtrials_json_2022-07-07.csv
#or
#clinicaltrials_raw_clincialtrials_json_2022-07-22.csv.zip

#For initial development, I'll use default headers, but could make this cutomisable.
#from lib.final_df import make_dataframe, headers
from lib.test_final_df import make_output, headers

#Load in the regulatory archive data
old_fda = 'data/fdaaa_regulatory_snapshot.csv'
fda_reg_dict = fda_reg(old_fda)

data_path = 'data/data_to_process'

#Get files to process
files = sorted(os.listdir(data_path))

#Also might be nice to check for the zipped-ness of the file
#Also, would be nice if we can get a file either locally or via a URL?
for fi in files:
    print(f'Processing File {fi}')
    #Making sc_date depends on the file name being the standard format to get the dates
    
    if '.zip' in fi:
        lines = get_data(data_path, fi, zipped=True)
        sc_date = datetime.strptime(fi.replace('.csv.zip','')[-10:], '%Y-%m-%d').date()
    else:
        lines = get_data(data_path, fi)
        sc_date = datetime.strptime(fi.replace('.csv','')[-10:], '%Y-%m-%d').date()
    
    #For now, lets just do it with the act_filter off for testing. Can do fancy things later.
    #Ideally, I should probably eventually move this to CSV writer as it will be much lower overhead than pandas
    #df = make_dataframe(tqdm(lines), fda_reg_dict, headers, act_filter=False, scrape_date = sc_date)
    make_output(tqdm(lines), fda_reg_dict, headers, act_filter=False, scrape_date = sc_date)
    
    del lines
    gc.collect()
    
    print(f'Completed File {fi}')
    #Will also need to find a way to make this dynamic
    #df.to_csv(f'data/output/ctgov_output_{sc_date}.csv')
    
    