'''
File: d:\github\Sequence-Design\CHIP2\analyses\figureMaking\code\replaceInterfaceColumn.py
Project: d:\github\Sequence-Design\CHIP2\analyses\figureMaking\code
Created Date: Saturday October 7th 2023
Author: gjowl
-----
Last Modified: Saturday October 7th 2023 7:48:19 pm
Modified By: gjowl
-----
Description:
Replaces the interface of the data file with the interface of the interface file. Since the interface is a number,
there are some times where I forgot to read it in as a string. So I need to go back to the file that has the 
original interface and replace the new file's interface column with the old file's interface column.
-----
'''

import os, sys, pandas as pd, argparse

# create the argument parser
parser = argparse.ArgumentParser(description='Append the interface of the data file with the interface of the interface file. Since the interface is a number, there are some times where I forgot to read it in as a string. So I need to go back to the file that has the original interface and replace the new file\'s interface column with the old file\'s interface column.')
# add the arguments
parser.add_argument('-interfaceFile', type=str, help='The file that contains the interface column that needs to be appended to the data file. The interface column should be a string.')
parser.add_argument('-dataFile', type=str, help='The file that contains the data that needs to be appended with the interface column.')
# add the optional arguments
parser.add_argument('-outputFile', type=str, help='The name of the output file that will be created.')
parser.add_argument('-outputDir', type=str, help='The directory where the output file will be created.')

# parse the arguments
args = parser.parse_args()
interfaceFile = args.interfaceFile
dataFile = args.dataFile
outputFile = 'output' if args.outputFile is None else args.outputFile
outputDir = os.getcwd() if args.outputDir is None else args.outputDir
os.makedirs(name=outputDir, exist_ok=True)

# read the input file and the file to merge as dataframes
interfaceDf = pd.read_csv(interfaceFile, sep=',', dtype={'Interface': str})
df = pd.read_csv(dataFile, sep=',')

# check if sequence length is 21
if len(df['Sequence'][0]) != 21:
    print('The sequence length is not 21, adding LLL and ILI to the ends.')
    # add LLL and ILI to the end of the sequences
    df['Sequence'] = df['Sequence'].apply(lambda x: 'LLL' + x + 'ILI')
# add interface column with value of None to df
df['Interface'] = None

# append the interface column with the interfaceDf interface column for matching sequences
for i in range(0, len(df)):
    # get the sequence
    sequence = df['Sequence'][i] # changed for the cpsf version from Directory
    # get the interface
    interface = interfaceDf[interfaceDf['Sequence'] == sequence]['Interface']
    # if the interface is not empty
    if len(interface) > 0:
        # replace the interface
        df['Interface'][i] = interface.values[0]

# output the dataframe to a csv file without the index
df.to_csv(f'{outputDir}/{outputFile}.csv', index=False)