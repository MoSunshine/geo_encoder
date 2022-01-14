# -*- coding: utf-8 -*-
"""
Created on Wed Jan 12 14:07:32 2022

@author: DE001E02544
"""
from geo_encoder.geo_encoder import geo_encoder
import sys

def main(file):
    geo_encoder_object = geo_encoder()
    geo_encoder_object.encode_location(file)
    
if __name__ == '__main__':
    main(sys.argv[1])
    
