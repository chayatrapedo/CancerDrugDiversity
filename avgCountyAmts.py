import pyspark

sc = pyspark.SparkContext()
sc.setLogLevel("ERROR")

a = sc.textFile('popNumPresc.data')

def pairs(line):
    fields = line.split('|')
    pop_size = ""
    pop = int(fields[0])
    if pop <= 100:         pop_size = 100     
    elif pop <= 1000:      pop_size = 1000    # a thousand
    elif pop <= 10000:     pop_size = 10000   # ten thousand
    elif pop <= 100000:    pop_size = 100000  # hundred thousand
    elif pop <= 1000000:   pop_size = 1000000 # a million
    else: pop_size = 10000000

    # size_category for population, (number of uniq drugs, 1 to count amount of counties and create circle size)
    return pop_size, (int(fields[1]), 1) # already uniqued in the previous step

def findMean(line):
    category = line[0]
    total_scripts = line[1][0]
    total_counties = line[1][1]

    return category, (total_scripts/total_counties, total_counties)


# Map all prescriptions to counties and a 1 to RBK
counties = a.map(pairs)
numInCategory = counties.reduceByKey(lambda x,y: (x[0] + y[0], x[1] + y[1]))
avg = numInCategory.map(findMean)
ans  = avg.sortByKey().collect()

# write output
with open('avgPoints.data', 'w') as f:
    for a in ans:
        f.write(f'{a[0]}|{a[1][0]}|{a[1][1]}|\n')
    f.close()
    





