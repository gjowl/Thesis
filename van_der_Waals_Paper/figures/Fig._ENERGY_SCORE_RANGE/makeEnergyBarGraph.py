import os, sys, argparse, pandas as pd, matplotlib.pyplot as plt

# initialize the parser
parser = argparse.ArgumentParser(description='Plot the frequency of energy scores for each design region')
# add the necessary arguments
parser.add_argument('-inFile','--inputFile', type=str, help='the input file')
# add the optional arguments
parser.add_argument('-outDir','--outputDir', type=str, help='the output directory')

# extract the arguments into variables
args = parser.parse_args()
inputFile = args.inputFile
# default values for the optional arguments
outputDir = os.getcwd()
# if the optional arguments are not specified, use the default values
if args.outputDir is not None:
    outputDir = args.outputDir
    os.makedirs(outputDir, exist_ok=True)

if __name__ == "__main__":
    # read in the data
    df = pd.read_csv(inputFile)
    # get the design regions
    regions = df['Region'].unique()
    # set the bin cutoffs for the histogram
    bins = [-60, -50, -40, -30, -20, -10, 0]
    # loop through the design regions
    for region in regions:
        # get the data for the region
        region_df = df[df['Region'] == region]
        # plot the frequency of energy scores
        plt.hist(region_df['Total'], bins=bins, edgecolor='black', linewidth=1.2, color='skyblue')
        # add the number of designs to the plot over each bin
        for i in range(len(bins)-1):
            numDesigns = len(region_df[(region_df['Total'] >= bins[i]) & (region_df['Total'] < bins[i+1])])
            plt.text(bins[i]+5, numDesigns, str(numDesigns))
        # add a title, x-axis label, and y-axis label
        plt.title(f'Frequency of Energy Scores for {region}')
        plt.xlabel('Energy Score')
        plt.ylabel('Frequency')
        # save the plot
        plt.savefig(f'{outputDir}/{region}_energyScoreFrequency.png')
        plt.savefig(f'{outputDir}/{region}_energyScoreFrequency.svg')
        plt.close()
