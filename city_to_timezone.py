import pandas as pd

# source file downloaded from http://download.geonames.org/export/dump/
file_path = '~/cities500.txt'

timezone_df = pd.DataFrame()

def initial_load_timezone_file(file_path):
    name = []
    asciiname = []
    alternatenames = []
    country_code = []
    timezone = []
    global timezone_df
    with open(file) as f:
        for line in f:
            data_line = []
            data_line = line.split("\t")
            name.append(data_line[1].lower())
            asciiname.append(data_line[2].lower())
            alternatenames.append(data_line[3].lower())
            country_code.append(data_line[8].upper())
            timezone.append(data_line[17])
    df = pd.DataFrame({'cityname':name, 'asciiname':asciiname, 'alternatenames':alternatenames, 'country_code':country_code, 'timezone':timezone})
    timezone_df = timezone_df.append(df, ignore_index = True)

def find_timezone_by(city, country):
    timezone = ''
    city = city.replace("市","").replace("city","").strip().lower()
    tz_df = timezone_df.loc[timezone_df['country_code'] == country.upper()]
    search_by_city = tz_df[tz_df['cityname'].str.contains(city)]
    if len(search_by_city) > 0:
        timezone = search_by_city['timezone'].iloc[0]
        return timezone
    search_by_asciiname = tz_df[tz_df['asciiname'].str.contains(city)]
    if len(search_by_asciiname) > 0:
        timezone = search_by_asciiname['timezone'].iloc[0]
        return timezone
    search_by_alternatenames = tz_df[tz_df['alternatenames'].str.contains(city)]
    if len(search_by_alternatenames) > 0:
        timezone = search_by_alternatenames['timezone'].iloc[0]
        return timezone
    return timezone

# initialize
initial_load_timezone_file(file_path)
# send ship_to_city, ship_to_country from the DN/Shipment, then get timezone
find_timezone_by("Taichung", "TW")
find_timezone_by("TAICHUNG", "TW")
find_timezone_by("taichung", "TW")
find_timezone_by("TaiCung", "TW")
find_timezone_by("台中市", "TW")
find_timezone_by("台中", "TW")
find_timezone_by("XXX", "TW")
find_timezone_by("ABC", "XXX")
