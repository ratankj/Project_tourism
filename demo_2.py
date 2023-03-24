from flask import Flask
from travelling.logger import logging
from travelling.exception import TravelException
import numpy as np
import pandas as pd
import os, sys
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    try:
        raise Exception("We are testing custom exception")
    except Exception as e:
        travelling = TravelException(e,sys)
        logging.info(travelling.error_message)
        logging.info("We are testing loggin module")
    return "Hello World"

if __name__=="__main__":
    app.run(debug = True)