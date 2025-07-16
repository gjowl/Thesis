import os, sys, pandas as pd, numpy as np, argparse
import matplotlib.pyplot as plt
from scipy.stats import ttest_ind

# initialize the parser
parser = argparse.ArgumentParser(description='Compare the vdw and sasa of mutants to the WT sequence')
parser.add_argument('-dataFile','--dataFile', type=str, help='the input reconstructed fluorescence csv file')
parser.add_argument('-outDir','--outputDir', type=str, help='the output directory')

# extract the arguments into variables
args = parser.parse_args()
# necessary arguments
dataFile = args.dataFile
# optional arguments
outputDir = os.getcwd()
if args.outputDir is not None:
    outputDir = args.outputDir
    os.makedirs(outputDir, exist_ok=True)

if __name__ == '__main__':
    # read in the data
    wt = pd.read_csv(dataFile, sep=',', dtype={'Interface': str})

    # check if sequence length is 21
    if len(wt['Sequence'][0]) != 21:
        print('The sequence length is not 21, adding LLL and ILI to the ends.')
        # add LLL and ILI to the end of the sequences
        wt['Sequence'] = wt['Sequence'].apply(lambda x: 'LLL' + x + 'ILI')
    
    
    # designate the columns to keep
    keepCols = ['Sequence', 'Total', 'Geometry', 'PercentGpA', 'PercentStd', 'Sample', 'toxgreen_fluor', 'toxgreen_std', 'interfaceSasa']
    wt = wt[keepCols]

    sig_figs = 2
    # combine the columns of value and stdev into one column, rounding to specified decimal places
    wt['PercentGpA'] = wt['PercentGpA'].round(sig_figs).astype(str) + ' ± ' + wt['PercentStd'].round(sig_figs).astype(str)
    wt.drop(columns=['PercentStd'], inplace=True)
    wt['toxgreen_fluor'] = wt['toxgreen_fluor'].round(sig_figs).astype(str) + ' ± ' + wt['toxgreen_std'].round(sig_figs).astype(str)
    wt.drop(columns=['toxgreen_std'], inplace=True)
    wt['Total'] = wt['Total'].round(sig_figs).astype(str)

    # sort the dataframe by the sample column
    wt = wt.sort_values(by='Total')
    wt = wt.sort_values(by='Sample')

    # for each sample, give a unique number to each sequence with at least two digits
    wt['Number'] = wt.groupby('Sample').cumcount() + 1
    wt['Number'] = wt['Number'].apply(lambda x: f'{x:03d}')

    # combine the Sample and Number columns into one column as a string
    wt['Sample'] = wt['Sample'].astype(str) + '_' + wt['Number'].astype(str)
    wt.drop(columns=['Number'], inplace=True)

    # rename the columns to their final names
    wt.rename(columns={'Sequence':'Sequence', 'Total':'Computational Score (kcal/mol)', 'PercentGpA':'GpA (%)', 'Sample':'Sample', 'toxgreen_fluor':'Reconstructed Fluorescence', 'interfaceSasa':'Interface SASA (Å)'}, inplace=True)
    # re-order the columns
    wt = wt[['Sample', 'Sequence', 'Computational Score (kcal/mol)', 'GpA (%)', 'Reconstructed Fluorescence', 'Interface SASA (Å)']]

    # save the dataframe as a pdf
    wt.to_csv(f'{outputDir}/pdf_data.csv', index=False)