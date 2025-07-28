import sys, os, pandas as pd, argparse

# initialize the parser
parser = argparse.ArgumentParser(description='Compare the vdw and sasa of mutants to the WT sequence')
parser.add_argument('-dataFile','--dataFile', type=str, help='the input reconstructed fluorescence csv file')
parser.add_argument('-outDir','--outputDir', type=str, help='the output directory')
parser.add_argument('-pdbDir','--pdbDir', type=str, help='the directory containing the pdb files')

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
    data = pd.read_csv(dataFile, sep=',', dtype={'Interface': str})

    # loop through rows
    for index, row in data.iterrows():
        # get the sample name and geometry
        sample_name, geometry = row['Sample'], row['Geometry']
        # separate geometry by underscore
        sequence, id = geometry.split('_')[0], geometry.split('_')[1]
        # get the path to the pdb file
        pdb_path = os.path.join(args.pdbDir, f"{sequence}/{id}.pdb")
        # check if the pdb file exists
        if os.path.exists(pdb_path):
            # copy the pdb file to the output directory
            output_pdb_path = os.path.join(outputDir, f"{sample_name}.pdb")
            with open(pdb_path, 'r') as pdb_file:
                with open(output_pdb_path, 'w') as output_file:
                    output_file.write(pdb_file.read())
            print(f"Copied {pdb_path} to {output_pdb_path}")
        else:
            print(f"PDB directory {args.pdbDir} does not exist, trying ala ends.")
            # change the first and last three letters to A in sequence
            sequence = 'A' * 3 + sequence[3:-3] + 'A' * 3
            pdb_path = os.path.join(args.pdbDir, f"{sequence}/{id}.pdb")
            if os.path.exists(pdb_path):
                output_pdb_path = os.path.join(outputDir, f"{sample_name}.pdb")
                with open(pdb_path, 'r') as pdb_file:
                    with open(output_pdb_path, 'w') as output_file:
                        output_file.write(pdb_file.read())
                print(f"Copied {pdb_path} to {output_pdb_path}")
            else:
                print(f"PDB file {pdb_path} does not exist. Skipping.")