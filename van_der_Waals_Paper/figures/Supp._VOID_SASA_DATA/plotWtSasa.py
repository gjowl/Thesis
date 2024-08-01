import os, sys, pandas as pd, numpy as np, argparse
import matplotlib.pyplot as plt
from scipy.stats import ttest_ind

# initialize the parser
parser = argparse.ArgumentParser(description='Compare the vdw and sasa of mutants to the WT sequence')
parser.add_argument('-wt','--wtFile', type=str, help='the input reconstructed fluorescence csv file')
parser.add_argument('-outDir','--outputDir', type=str, help='the output directory')

# extract the arguments into variables
args = parser.parse_args()
# necessary arguments
wtFile = args.wtFile
# optional arguments
outputDir = os.getcwd()
if args.outputDir is not None:
    outputDir = args.outputDir
    os.makedirs(outputDir, exist_ok=True)

if __name__ == '__main__':
    # read in the data
    wt = pd.read_csv(wtFile)

    # rid of proteins that have a positive energy (sequences where bbOptimization of the structure was poor)
    wt = wt[wt['VDWDiff'] < 0]

    # sort by the sample column
    wt = wt.sort_values(by='Sample')

    # plot the interfaceSasa as a boxplot for each sample
    fig, ax = plt.subplots()
    ax = wt.boxplot(column='interfaceSasa', by='Sample', ax=ax)
    # plot the individual points over the boxplot in the same order of the boxplot
    for i, sample in enumerate(wt['Sample'].unique()):
        tmp = wt[wt['Sample'] == sample]
        x = np.random.normal(i+1, 0.04, size=len(tmp))
        ax.plot(x, tmp['interfaceSasa'], 'o', alpha=0.5)
    plt.title('Interface SASA')
    plt.ylabel('SASA (Å²)')
    plt.xlabel('Sample')
    plt.xticks(rotation=45)
    plt.savefig(f'{outputDir}/interfaceSasa.png')
    plt.savefig(f'{outputDir}/interfaceSasa.svg')
    # use a t-test to determine if the means are significantly different
    samples = wt['Sample'].unique()
    for i in range(len(samples)-1):
        for j in range(i+1, len(samples)):
            sample1 = samples[i]
            sample2 = samples[j]
            s1 = wt[wt['Sample'] == sample1]['interfaceSasa']
            s2 = wt[wt['Sample'] == sample2]['interfaceSasa']
            t, p = ttest_ind(s1, s2)
            plt.text(i+1, 0.5, f'{sample1} vs {sample2}\np-value: {p}', ha='center', va='center', fontsize=8, color='red')
    plt.tight_layout()
    plt.savefig(f'{outputDir}/interfaceSasa_sig.png')
    plt.savefig(f'{outputDir}/interfaceSasa_sig.svg')
