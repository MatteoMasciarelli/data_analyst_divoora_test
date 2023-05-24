import pandas as pd
import sqlite3
from pydantic import ValidationError
import json
from models import OrderTiming, GeoData, Address, ValidatedData

# This pipeline assumes that the data is provided on a regular basis 
# The format of the data is the same
# It is assumed that the completed dataset is provided at every load

# A streamlined version of an ETLPipeline is being constructed

class ETLPipeline:
    def __init__(self, filename: str, H: str) -> None:
        # Source information
        self.filename : str = filename
        
        # Target information
        self.host : str = H

        # Helper objects
        self.validated_data : ValidatedData = ValidatedData

    def extract(self):
        # connect to excel file
        df = pd.read_excel(self.filename, None)
        
        sheet_names = ['tempistiche_ordini', 'dai_geospaziali', 'address_driver']

        # Validate all data and store in validated data object
        for sheet in sheet_names:
            if sheet == 'address_driver':
                a = []
                for i in json.loads(df.get(sheet).to_json(orient = 'records')):
                    try:
                        a.append(Address(**i))
                    except ValidationError: 
                        print('Address Validation Error, data not valid')

                self.validated_data.address = a
            if sheet == 'dai_geospaziali':
                g = []
                new_cols = ['order_id', 'driver_id', 'shift_id', 'origin_id', 'pickup_id',
                            'destination_id', 'distance', 'lat_x', 'lng_x', 'lat_y', 'lng_y', 'lat',
                            'lng']
                holder_df = df.get(sheet)
                holder_df.columns = new_cols
                for i in json.loads(holder_df.to_json(orient = 'records')):
                    try:
                        g.append(GeoData(**i))
                    except ValidationError: 
                        print('Geographic Validation Error, data not valid')
                self.validated_data.geo_data = g
            if sheet == 'tempistiche_ordini':
                t = []
                for i in json.loads(df.get(sheet).to_json(orient = 'records')):
                    try:
                        t.append(OrderTiming(**i))
                    except ValidationError: 
                        print('Timing Validation Error, data not valid')
                self.validated_data.order_timing = t        

    def transform(self) -> None:
        # Custom transformation is applied to the data
        # We do not require any transformation in this case!
        pass

    def load(self) -> None:
        # Load data into data frame
        geo_df = pd.DataFrame.from_records([i.dict() for i in self.validated_data.geo_data])
        timing_df = pd.DataFrame.from_records([i.dict() for i in self.validated_data.order_timing])
        address_df = pd.DataFrame.from_records([i.dict() for i in self.validated_data.address])
        
        # Upload data to database
        with sqlite3.connect('Divoora.db') as conn:
            geo_df.to_sql('geo_data', conn, if_exists='replace', index=False)
            timing_df.to_sql('order_timing', conn, if_exists='replace', index = False)
            address_df.to_sql('address', conn, if_exists='replace', index = False)
        
if __name__ == '__main__':
    # Test if it works
    e = ETLPipeline("database.xlsx","Divoora.db")
    e.extract()
    e.load()