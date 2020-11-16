import os
import glob
import urllib.request 
import pandas as pd
from urllib.parse import urlparse

def download_data(url, to_dataframe=False):
    '''
    Downloads a file and save it to the cwd.
    
    Keyword arguments:
    url             --  url of the file
    to_dataframe    --  (default False) if True, create a pandas dataframe 
                        if the downloaded file is .csv

    '''
    file_name = os.path.basename(urlparse(url).path)
    urllib.request.urlretrieve(url, file_name)
    if to_dataframe:
        if file_name[-4:]!='.csv':
            print('Pandas dataframe not created as file is not .csv \n' + 
            str(file_name) + ' downloaded and saved to ' + str(os.getcwd()))   
        else:
            csv_path = os.path.join(os.getcwd(), file_name)
            print(str(file_name) + ' downloaded and saved to ' + str(os.getcwd()))
            return pd.read_csv(csv_path)
    else:
        print(str(file_name) + ' downloaded and saved to ' + str(os.getcwd()))

    #todo - new karg for downloading to specific location


def load_single_csv(file_name, file_path=os.getcwd()):
    '''
    Loads a single csv file into a pandas dataframe

    Keyword arguments:
    file_path   --  (default cwd) the file path if not in the current working directory
    file_name   --  name of file 
                    e.g. "file.csv"

    '''
    if file_name[-4:]!='.csv':
        file_name+='.csv'
    return pd.read_csv(os.path.join(file_path, file_name))


def load_multiple_csv(file_path, file_name_as_column=False):
    '''
    Load multiple .csv files with the same structure into a single Pandas dataframe

    Keyword arguments:
    file_path           --  file path of all files 
                            e.g. "C:\\Users\\User1\\ML\\Dataset\\Train"
    file_name_as_column --  add a column to the end of the dataframe named 'filename' 
                            and insert the file the row belongs to.
    '''
    all_files = glob.glob(file_path + '/*.csv')
    list_of_files = [] 
    for filename in all_files:
        df = pd.read_csv(filename, index_col=None, header=0)
        if file_name_as_column:
            df['filename'] = os.path.basename(filename)[:-4] #add filename as column
        list_of_files.append(df)

    return pd.concat(list_of_files, axis=0, ignore_index=True)


