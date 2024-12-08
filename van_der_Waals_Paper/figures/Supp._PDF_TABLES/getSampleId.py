import os, sys, pandas as pd, argparse

# create the argument parser
parser = argparse.ArgumentParser(description='Replace the sample id with the id from the all samples file (wt or mutant).')

# add the arguments
parser.add_argument('-allSamplesFile', type=str, help='The file that contains all the samples and their ids.')
parser.add_argument('-dataFile', type=str, help='The file that contains the data that needs to be appended with the sample id.')

# add the optional arguments
parser.add_argument('-outputFile', type=str, help='The name of the output file that will be created.')
parser.add_argument('-outputDir', type=str, help='The directory where the output file will be created.')

# parse the arguments
args = parser.parse_args()
allSamplesFile = args.allSamplesFile
dataFile = args.dataFile
# get the name of the data file without the extension
dateFileName = dataFile.split('/')[-1].split('.')[0]
outputFile = f'{dateFileName}_correct_sample_id' if args.outputFile is None else args.outputFile
outputDir = os.getcwd() if args.outputDir is None else args.outputDir
os.makedirs(name=outputDir, exist_ok=True)

# read the input file and the file to merge as dataframes
allSamplesDf = pd.read_csv(allSamplesFile, sep=',')
df = pd.read_csv(dataFile, sep=',')

# replace sample id with the id from the all samples file
#df['Sample'] = df['Sequence'].apply(lambda x: allSamplesDf[allSamplesDf['Sequence'] == x]['Sample'].values[0])
for i in range(0, len(df)):
    # get the sequence
    sequence = df['Sequence'][i]
    # get the id
    sample = allSamplesDf[allSamplesDf['Sequence'] == sequence]['Sample'].values[0]
    # replace the id
    df['Sample'][i] = sample

# replace any missing values in the entire dataframe with NA
df = df.fillna('NA')

# save the dataframe as a csv
df = df.sort_values(by='Sample')
df.to_csv(f'{outputDir}/{outputFile}.csv', index=False)