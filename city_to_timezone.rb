require 'daru'

# source file downloaded from http://download.geonames.org/export/dump/
file_path = '~/cities500.txt'

$timezone_df = Daru::DataFrame.new()

def initial_load_timezone_file(file_path)
  name = []
  asciiname = []
  alternatenames = []
  country_code = []
  timezone = []
  File.open(file_path).each do |line|
    line = line.split("\t")
    name.append(line[1].downcase)
    asciiname.append(line[2].downcase)
    alternatenames.append(line[3].downcase)
    country_code.append(line[8].upcase)
    timezone.append(line[17])
  end
  $timezone_df['cityname'] = name
  $timezone_df['asciiname'] = asciiname
  $timezone_df['alternatenames'] = alternatenames
  $timezone_df['country_code'] = country_code
  $timezone_df['timezone'] = timezone
end

def find_timezone_by(city, country)
  timezone = ''
  city = city.gsub("市", "").gsub("city","").strip().downcase
  tz_df = $timezone_df.where($timezone_df['country_code'].eq(country.upcase))
  tz_df.where(tz_df['cityname'].map{|row| row.include?(city)}).first.timezone.first or
  tz_df.where(tz_df['asciiname'].map{|row| row.include?(city)}).first.timezone.first or
  tz_df.where(tz_df['alternatenames'].map{|row| row.include?(city)}).first.timezone.first or ''
end

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
