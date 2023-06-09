import shutil

import sys,os
from travelling.exception import TravelException
from travelling.logger import logging

import tarfile
import numpy as np
from six.moves import urllib
import urllib.request
import pandas as pd
from datetime import date
from sklearn.model_selection import train_test_split
from travelling.config.cofiguration import Configuration
from travelling.entity.config_entity import DataIngestionConfig
from travelling.entity.artifact_entity import DataIngestionArtifact
from sklearn.model_selection import StratifiedShuffleSplit

class DataIngestion:

    def __init__(self,data_ingestion_config:DataIngestionConfig ):
        try:
            logging.info(f"{'>>'*20}Data Ingestion log started.{'<<'*20} ")
            self.data_ingestion_config = data_ingestion_config

        except Exception as e:
            raise TravelException(e,sys)
    

    def download_travel_data(self,) -> str:
        try:
            #extraction remote url to download dataset
            download_url = self.data_ingestion_config.dataset_download_url

            #folder location to download file
            raw_data_dir = self.data_ingestion_config.raw_data_dir
            
            os.makedirs(raw_data_dir,exist_ok=True)

            travel_file_name = os.path.basename(download_url)

            raw_file_path = os.path.join(raw_data_dir, travel_file_name)

            logging.info(f"Downloading file from :[{download_url}] into :[{raw_file_path}]")
            urllib.request.urlretrieve(download_url,raw_file_path)
            logging.info(f"File :[{raw_file_path}] has been downloaded successfully.")
            return raw_file_path

        except Exception as e:
            raise TravelException(e,sys) from e
        


    
    def split_data_as_train_test(self) -> DataIngestionArtifact:
        try:
            raw_data_dir = self.data_ingestion_config.raw_data_dir

            file_name = os.listdir(raw_data_dir)[0]

            travel_file_path = os.path.join(raw_data_dir,file_name)



            logging.info(f"Reading csv file: [{travel_file_path}]")

            today_date = date.today()
            travel_data_frame = pd.read_csv(travel_file_path)

            #travel_data_frame.drop([COLUMN_Customer_ID] , axis=1,inplace=True)         

            logging.info(f"Splitting data into train and test")

            strat_train_set = None
            strat_test_set = None

# train test split

#************************************************************************************
            #X=travel_data_frame.drop("MonthlyIncome",axis=1)
            #y=travel_data_frame['MonthlyIncome']

            strat_train_set,strat_test_set =train_test_split(travel_data_frame,test_size =0.2 ,random_state=42)

            #split = StratifiedShuffleSplit(n_splits=1, test_size=0.2, random_state=42)

            #for train_index,test_index in split.split(travel_data_frame,travel_data_frame["MonthlyIncome"]):
            #for train_index,test_index in split.split(X,y):
             #   strat_train_set = travel_data_frame.loc[train_index]
              #  strat_test_set = travel_data_frame.loc[test_index]

            train_file_path = os.path.join(self.data_ingestion_config.ingested_train_dir,
                                            file_name)

            test_file_path = os.path.join(self.data_ingestion_config.ingested_test_dir,
                                        file_name)



#***************************************************************************************************************************

            if strat_train_set is not None:
                os.makedirs(self.data_ingestion_config.ingested_train_dir,exist_ok=True)
                logging.info(f"Exporting training datset to file: [{train_file_path}]")
                strat_train_set.to_csv(train_file_path,index=False)

            if strat_test_set is not None:
                os.makedirs(self.data_ingestion_config.ingested_test_dir, exist_ok= True)
                logging.info(f"Exporting test dataset to file: [{test_file_path}]")
                strat_test_set.to_csv(test_file_path,index=False)
            

            data_ingestion_artifact = DataIngestionArtifact(train_file_path=train_file_path,
                                test_file_path=test_file_path,
                                is_ingested=True,
                                message=f"Data ingestion completed successfully."
                                )
            logging.info(f"Data Ingestion artifact:[{data_ingestion_artifact}]")
            return data_ingestion_artifact

        except Exception as e:
            raise TravelException(e,sys) from e

    def initiate_data_ingestion(self)-> DataIngestionArtifact:
        try:
            raw_file_path =  self.download_travel_data()
            
            return self.split_data_as_train_test()
        
        except Exception as e:
            raise TravelException(e,sys) from e

