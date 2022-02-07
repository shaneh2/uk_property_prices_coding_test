import pandas as pd

RAW_DATA_LOCATION = "../data/full_data_csv.csv"
FULL_DATA_FEATHER_PATH = "../data/full_data_feather.feather"
# TODO: change this boolean when putting in all data, which might not contain the 'Record_status' field
IGNORING_MONTHLY_UPDATE_FIELD = False

columns_dict = {'UID': str,
                'Price': int,
                'Date_of_transfer': str,
                'Postcode': str,
                'Property_type': str,
                # Property Type: D = Detached, S = Semi-Detached, T = Terraced, F = Flats/Maisonettes, O = Other
                'Old_or_new': str,  # Y = a newly built property, N = an established residential building
                'Duration': str,  # Relates to the tenure: F = Freehold, L= Leasehold etc.
                'PAON': str,  # Primary Addressable Object Name. Typically the house number or name.
                'SAON': str,
                # Secondary Addressable Object Name. Where a property has been divided into separate units (for example,
                # flats), the PAON (above) will identify the building and a SAON will be specified that identifies
                # the separate unit/flat.
                "Street": str,
                "Locality": str,
                "Town_city": str,
                "District": str,
                "County": str,
                "PPD_cat": str,
                "Record_status": str}
if IGNORING_MONTHLY_UPDATE_FIELD:
    del columns_dict["Record_status"]
full_df = pd.read_csv(RAW_DATA_LOCATION,
                      names=list(columns_dict.keys()),
                      dtype=columns_dict,
                      sep=',',
                      index_col=False)
full_df['Date_of_transfer'] = pd.to_datetime(full_df['Date_of_transfer'])  # https://stackoverflow.com/a/26763793
full_df.reset_index().to_feather(FULL_DATA_FEATHER_PATH)
