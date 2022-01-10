import json
import numpy as np
import pandas as pd
from shapely.geometry import shape, mapping
from shapely.ops import transform
import pyproj


def load_geojson(fp):
    data = json.load(fp)
    df = []
    for feature in data["features"]:
        track_id = feature["properties"]["track_id"]
        df.append({
            "track_id": track_id, 
            "geometry_type": feature["geometry"]["type"], 
            "geometry": feature["geometry"]
        })
    df = pd.DataFrame(df)
    return df


def save_geojson(df, fp):
    """Takes a pandas DataFrame with a 'geometry' column containing shapely geometries in WGS84 coordinates.
    Each row of the dataframe represents one GeoJSON feature. The dataframe may contian additional columns, 
    which are written into the properties of the feature."""
    features = []

    df = df.reset_index()
    df = df.where(pd.notnull(df), None)  # replace nan with None
    records = df.to_dict('records')
    for record in records:
        # assemble feature
        feature = {
            'type': 'Feature',
            'geometry': {
                'type': record['geometry_type'],
                'coordinates': record['geometry']["coordinates"]
            },
            'properties': {}
        }
        
        # insert properties
        for k, v in record.items():
            if k in ['index', 'level_0', 'geometry', 'geometry_type']:
                continue
            feature['properties'][k] = v            
        
        features.append(feature)
    
    geojson = {
        'type': 'FeatureCollection',
        'crs': {
            'type': 'name',
            'properties': {
                'name': 'urn:ogc:def:crs:OGC:1.3:CRS84'
            }
        },
        'features': features
    }
    json.dump(geojson, fp)


def coords_wgs84_to_ltp(df):
    """Convert dataframe from WGS84 to LTP."""
    wgs84 = pyproj.CRS('EPSG:4326')
    ltp = pyproj.CRS('EPSG:3857')
    projection = pyproj.Transformer.from_crs(wgs84, ltp, always_xy=True).transform
    # apply transform
    geometry_transformed = []
    for geometry in df.loc[:, "geometry"]:
        geometry = transform(projection, shape(geometry))
        geometry = mapping(geometry)
        geometry["coordinates"] = np.array(geometry["coordinates"]).tolist()
        geometry_transformed.append(geometry)
    df_transformed = df.copy()
    df_transformed.loc[:, "geometry"] = geometry_transformed
    return df_transformed