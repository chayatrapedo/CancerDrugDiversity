import gzip
# lookup county population from 2022 census data
def county_lookup_dictionary(filename):
    
    # unzip and load
    lookup = {}
    with gzip.open(filename, 'rt') as f:
        
        for line in f:
            
            fields = line.split('|')
            county = fields[0]
            population = int(fields[1])
            lookup[county] = population
        return lookup

def main():

    # load input file
    # uszips pass string to each
    lookup = county_lookup_dictionary("estPop2022.gz")
    
    # load and match to county
    with open('countyCounts', 'r') as f:

        # only include counties in US census data (estPop2022.gz)
        for line in f:
            fields = line.split("|")
            county = fields[0]
            if county in lookup: # if county is in census data, use census population est.
                print(f'{lookup[county]}|{fields[1]}')

main()
