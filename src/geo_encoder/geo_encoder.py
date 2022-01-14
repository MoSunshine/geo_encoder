# -*- coding: utf-8 -*-
"""
Created on Wed Jan 12 11:36:10 2022

@author: moritz.wegener- moritz.wegener@uni-koeln.de
Class to get the latitude and longitude of a datset based on the adress, zip code, country and city

"""
import pandas as pd
import requests
import json
import time
import logging
import traceback


class geo_encoder():
    """
    
    """
    def __init__(self):
        self.logger = logging.Logger('Logging')
        fh = logging.FileHandler("../log/errors.log")
        fh.setLevel(logging.INFO)
        fh.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))
        self.logger.addHandler(fh)
    
    
    def read_dataset(self,file):
        path = "../"+file
        try:
            dataset = pd.read_csv(path, sep=",", encoding="utf-8", dtype={"street":str,"zip_code":str,"country":str,"city":str})
            return dataset
        except Exception as e:
            self.logger.error('Error reading input data ' + file +".")
            self.logger.error(traceback.format_exc())
            
            
    def encode_location(self,file):
        ###build search string###
        dataset = self.read_dataset()
        print(dataset)
        dataset["search_url"] = "https://nominatim.openstreetmap.org/search?"+"street="+dataset["street"]+"&city="+dataset["city"]+"&country=Germany&postalcode="+dataset["zip_code"]+"&addressdetails=1&extratags=1&namedetails=1&format=json"
        url_list = dataset["search_url"].tolist()
        result_list_lat = []
        result_list_lon= []
        i = 0
        for url in url_list:
            i +=1
            print("Encode "+ str(i) + " of "+ str(len(url_list)))
            try:
                page = requests.get(url).text
                json_object = json.loads(page)
                time.sleep(1)
                result_list_lat.append(json_object[0]["lat"])
                result_list_lon.append(json_object[0]["lon"])
            except Exception as e:
                self.logger.error('Error reading url '+url + " of file "+ file)
                self.logger.error(traceback.format_exc())
        dataset["lat"] = result_list_lat
        dataset["lon"] = result_list_lon
        dataset.to_csv("../results/" +file+"_endocded.csv",encoding="utf-8",sep=",",index=False)