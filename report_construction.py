import sqlite3
import pandas as pd
import geopy.distance

def get_query(queryName):
    with open(queryName) as f:
        query = f.read()

    return query

def perform_query(queryName):
    updated = queryName+'.sql'
    query = get_query(updated)
    with sqlite3.connect("Divoora.db") as conn:
        df = pd.read_sql(query, conn)

    if queryName == 'distanze':
        op = []
        pi_d = []

        for i, row in df.iterrows():
            origin_ = (row['origin_lat'], row['origin_lon'])
            pickup_ = (row['pickup_lat'], row['pickup_lng'])
            destination_ = (row['destination_lat'], row['destination_lng'])

            op.append(geopy.distance.geodesic(origin_, pickup_).km)
            pi_d.append(geopy.distance.geodesic(pickup_, destination_).km)

        df['origin_pickup'] = op
        df['pickup_destination'] = pi_d

        df['total_distance'] = df['origin_pickup'] + df['pickup_destination']


    df.to_csv(queryName+'.csv', index = False)

def perform_both():
    qs = ['tempistiche','distanze']

    for q in qs:
        perform_query(q)

if __name__ == '__main__':
    perform_query('tempistiche')