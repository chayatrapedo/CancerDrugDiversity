# Load array (key = NPI, data = city, state, zip)
function loadArray(command, array, name) {
    while ((command | getline) > 0) {
        
        # NPI file fields
        # 1 = NPI Numbers
        # 25 = ZIP
	# 33 = Backup ZIP

        npi   = $1
	zip   = substr($25,5)
        # Assign location tuple to each NPI
        array[npi] = zip

	if (array[npi] == "") { # if no primary zip
	    # use alt zip
	    array[npi] = substr($33, 5)
	}
	
	
    }
    close(command) # Close the command after processing
}

BEGIN {
    # Field separators
    FS = "|"
    OFS = "|"

    # Load NPI locations array
    npiFile = "NPI.gz"
    npiCommand = "zcat " npiFile
    loadArray(npiCommand, locations)

    # load NPIcancerPrescriptions.gz and connect prescription to
    # location via shared NPI
    cancerDrugsFile = "NPIcancerPrescriptions.gz"
    drugsCommand = "zcat " cancerDrugsFile
    outputCommand = "gzip > prescLocations.gz"
    
    while ((drugsCommand | getline) > 0) {

	# extract current NPI
	npi = $1

	zip = locations[npi]
	#     ZIP  | CITY | STATE |  BRAND | GENERIC
	print zip "|" $4 "|" $5  "|"  $2  "|" $3 "|"| outputCommand
    }
    close(drugsCommand)



}
