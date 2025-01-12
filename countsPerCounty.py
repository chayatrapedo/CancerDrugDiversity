import pyspark

sc = pyspark.SparkContext()
sc.setLogLevel("ERROR")

a = sc.textFile('prescCounties.gz')

def pairs(line):
    county = line.split('|')
    return county[0], 1 # already uniqued in the previous step

# Map all prescriptions to counties and a 1 to RBK since already uniqued by county, drug in command line
counties = a.map(pairs)
sums     = counties.reduceByKey(lambda x,y: x+y)
ans      = sums.collect()

# write output
with open('countyCounts', 'w') as f:
    for a in ans:
        f.write(f'{a[0]}|{a[1]}|\n')
    f.close()





