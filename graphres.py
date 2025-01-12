import matplotlib.pyplot as plt

# Initialize lists for coordinates and point sizeson each axis
population_x, drug_diversity_y, sizes =  [], [], []

# Read in file with data points and allocate to each list
with open('avgPoints.data', 'r') as f:
    for line in f:
        fields = line.strip().split('|')
        population_x.append(int(fields[0]))
        drug_diversity_y.append(float(fields[1]))
        sizes.append(int(fields[2]))



# Get total number of data points
N = len(population_x)

# Add to figure object to label data points later
fig = plt.figure(figsize=(10, 6))  # Adjust figure size
ax = fig.add_subplot(111)

# Log scale for graph
plt.xscale('log', base=10)
plt.yscale('log', base=10)

plt.xticks(population_x, ['≤100','≤1,000','≤10,000','≤100,000', '≤1,000,000', '>1,000,000'])

# Plot
plt.scatter(population_x, drug_diversity_y, c='c', alpha=0.5, s=sizes)

# Label axis
plt.xlabel("County Population")
plt.ylabel("Average Amount of Unique Cancer Drug Prescriptions per County")
plt.title("Relationship Between Diversity of Prescribed Cancer Drugs and Population")

# Center labels of number of counties per category on each point
for i, amt in enumerate(sizes):
    ax.annotate(amt, (population_x[i], drug_diversity_y[i]),
                xytext=(0,0),
                textcoords='offset points',
                ha='center',  # Horizontal alignment
                va='center')  # Vertical alignment

# Create a legend explaining the size of the points
legend_sizes = [100, 500, 1500]  # Example marker sizes
legend_labels = ['100 counties', '500 counties', '1500 counties']

# Add custom legend markers
plt.scatter([], [], c='c', alpha=0.5, s=100, label=f"size of point = number of counties out of {sum(sizes)} counties")

# Position the legend below the plot
plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.2), ncol=3, title="Point Sizes")

# Adjust layout to ensure everything fits
plt.tight_layout()
fig.subplots_adjust(bottom=0.3)  # Add extra space at the bottom for the legend

# Save results to PDF
plt.savefig("Cancer_Drug_Diversity_by_County_Results.pdf")
plt.show()
