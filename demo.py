from travelling.pipeline.pipeline import Pipeline
from travelling.exception import TravelException
from travelling.logger import logging
from travelling.config.cofiguration import Configuration
from travelling.components.data_ingestion import DataIngestion
import os


def main():
    try:
        config_path = os.path.join("config","config.yaml")
        pipeline = Pipeline(Configuration(config_file_path=config_path))
        #pipeline = Pipeline()
        pipeline.run_pipeline()
       
    except Exception as e:
        logging.error(f"{e}")
        print(e)



if __name__=="__main__":
    main()