import os, sys, pandas as pd, numpy as np, argparse, matplotlib.pyplot as plt

# initialize the parser
parser = argparse.ArgumentParser(description='Compare two files and keep matching sequences')
# add the necessary arguments
parser.add_argument('-file1','--file1', type=str, help='the first file')
parser.add_argument('-file2','--file2', type=str, help='the second file that has sequences to keep')

# extract the arguments into variables
args = parser.parse_args()
file1 = args.file1
file2 = args.file2

if __name__ == '__main__':
    # read in the data
    df1 = pd.read_csv(file1)
    df2 = pd.read_csv(file2)
    # get the sequences from the second file
    sequences = df2['Sequence'].unique()
    # keep only the sequences that match
    df1 = df1[df1['Directory'].isin(sequences)]
    # add the region from df2 to df1
    df1['Region'] = df1['Directory'].apply(lambda x: df2[df2['Sequence'] == x]['Region'].values[0])
    # save the file
    df1.to_csv('matchingSequences.csv', index=False)