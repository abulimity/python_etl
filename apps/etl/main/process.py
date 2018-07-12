import os
import csv

from python_etl.settings import MEDIA_ROOT

class Process():
    def __init__(self):
        self.update_dir = MEDIA_ROOT + r'upload\etl'

    def processCSV(self,file):
        if file =='':
            r = 'none'
        else:
            r = file
        return  r