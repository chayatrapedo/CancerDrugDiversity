import gzip
# adjust parameters accordingly, can look up by city or by zip code
def county_lookup_dictionary(filename):

    # unzip and load
    lookup = {}
    with gzip.open(filename, 'rt') as f:
        
        for line in f:
            
            line = line.strip()
            fields = line.split('|')
            city = fields[0]
            state = fields[1]
            county = fields[2]
            zips = fields[4].split()
            data = f'{county} COUNTY, {state}'
            
            for z in zips:
                lookup[z] = data

            city_key = f'{city}|{state}'
            lookup[city_key] = data
            
        return lookup

def main():

    # load input file
    # uszips pass string to each
    lookup = county_lookup_dictionary("uszips.gz")
    
    # load and match zip to county
    with gzip.open('prescLocations.gz', 'rt') as f:
    
        for line in f:
            fields = line.split("|")
            zip = fields[0]
            # attempt to find county by zip
            if zip in lookup:
                print(f'{lookup[zip]}|{fields[3]}/{fields[4]}')
            else:
                # attempt to find county by city|state combo key
                citykey = f'{fields[1]}|{fields[2]}'
                if citykey in lookup:
                    print(f'{lookup[citykey]}|{fields[3]}/{fields[4]}')                
main()
