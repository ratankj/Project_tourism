from collections import namedtuple
from datetime import datetime
from travelling.config.cofiguration import Configuration
from travelling.logger import logging
from travelling.exception import TravelException
from threading import Thread
from typing import List
import os, sys
from multiprocessing import Process
from travelling.entity.artifact_entity import DataIngestionArtifact
from travelling.entity.config_entity import DataIngestionConfig
from travelling.components.data_ingestion import DataIngestion


class Pipeline:
   
     def __init__(self, config: Configuration = Configuration() ) -> None:
        try:
            self.config = config

        except Exception as e:
            raise TravelException(e, sys) from e

     def start_data_ingestion(self) -> DataIngestionArtifact:
        try:
            data_ingestion = DataIngestion(data_ingestion_config=self.config.get_data_ingestion_config())
            return data_ingestion.initiate_data_ingestion()
        except Exception as e:
            raise TravelException(e, sys) from e
        

     def run_pipeline(self):
         try:
             #data ingestion

             data_ingestion_artifact = self.start_data_ingestion()
             
         except Exception as e:
             raise TravelException(e, sys) from e