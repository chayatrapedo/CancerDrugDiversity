# Generate scatterplot of the county categories spanning the 5480 unique counties
all: Cancer_Drug_Diversity_by_County_Results.pdf

Cancer_Drug_Diversity_by_County_Results.pdf: avgPoints.data graphres.py
	python3 graphres.py


# Average number of unique prescriptions per county population category (<100, <=1000, etc.)
avgPoints.data: avgCountyAmts.py popNumPresc.data
	python3 avgCountyAmts.py


# Convert county to estimated population based on census data
popNumPresc.data: countyPopulations.py countyCounts
	python3 countyPopulations.py > popNumPresc.data


# Using PySpark to reduce by key for each unique prescription
countyCounts: countsPerCounty.py prescCounties.gz
	python3 countsPerCounty.py

# Outputs ('COUNTY', 'STATE')|BRAND/GENERIC on every line, matching zip or city/state to county
# uniqs the the answers to measure the amount of unique prescriptions prescribed per county
prescCounties.gz: uszips.gz prescLocations.gz countyMatching.py
	python3 countyMatching.py | sort | uniq | gzip  > prescCounties.gz


# Clean uszips file and takes data relevant for calculations, resulting in
# CITY | STATE | COUNTY | POPULATION | [List of Zip Codes in the County)
uszips.gz: uszips.csv
	cat uszips.csv | tr [:lower:] [:upper:] | tr -d "\"" | tr -d "\." | tr -s "," "|" | cut -d "|" -f 1,4,6,9,16 | gzip > uszips.gz


# Outputs ZIP | CITY | STATE | BRAND | GENERIC, matching prescription location
# to zip based on NPI.gz
prescLocations.gz: NPI.gz NPIcancerPrescriptions.gz CancerPrescNPILocations.awk
	gawk -f CancerPrescNPILocations.awk
	echo "Matched all cancer-prescriptions to locations"

# Outputs NPI | BRAND | GENERIC | CITY | STATE for matching entries
# in Prescriptions.gz based on the cancerDrugsList
NPIcancerPrescriptions.gz: Prescriptions.gz cancerDrugsList.txt prescCancerDrugNPI.awk
	gawk -f prescCancerDrugNPI.awk
	echo "Found all cancer-related prescriptions in Prescriptions.gz"

# Remove files created from the pipeline
clean:
	rm NPIcancerPrescriptions.gz prescLocations.gz uszips.gz prescCounties.gz \
	countyCounts popNumPresc.data avgPoints.data Cancer_Drug_Diversity_by_County_Results.pdf

# Not in the pipeline:
# prescCancerProviders.awk -> extracts prescriptions from
# Prescriptions.gz where the provider is oncology-related based
# prescCancerProvidersList.txt list.
# Outputs prescCancerProvidersList.txt

# Cut the brand, generic fields 9 and 10, and eyeball
# checked each drug that was used for only cancer treatments (without
# overlap for other diseases, i.e. Prednisone to treat rheumatoid arthritis
# or other prescriptions for conditions that are being treated alongside cancer
# by the oncologist (Gabapentin for muscle-relaxants, etc.)
# Outputs cancerDrugsList.txt

#################


