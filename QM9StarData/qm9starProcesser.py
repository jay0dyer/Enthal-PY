import pandas as pd
from rdkit import Chem
from concurrent.futures import ProcessPoolExecutor
import os
import sys
import ast
from xyzgraph import build_graph_rdkit

# orginal csv isnt on github as its not nesseray to the project
csv = "qm9star_raw.csv"

final_csv = "SMILESEnthalpyLookUp.csv"

# so this is a lot of data to process so want minimual load on my laptops ram and cpu so im going to split into chunks
# and across 8 cpu cores
chunk_size = 50000
num_cores = max(1, os.cpu_count() - 4)

fomatter = lambda text : text.translate(str.maketrans({"{":"[","}":"]"})).replace("nan","None")
BondOrders = {1:Chem.BondType.SINGLE, 2:Chem.BondType.DOUBLE, 3:Chem.BondType.TRIPLE, 12:Chem.BondType.AROMATIC}


# this is borrowed code to mute xyz2mols output

def init_worker():
    """ Runs once when each CPU process is spawned, permanently muting it. """
    import xyz2mol  # Import inside the worker so it respects the muted stdout
    #sys.stdout = open(os.devnull, 'w')

def createSmiles(atoms, bonds, formal_charges, formal_num_radicals):
    mol = Chem.RWMol()
    radicalType = 0
    for atom, charge, radical in zip(atoms, formal_charges, formal_num_radicals):
        AtomObj = Chem.Atom(atom)
        AtomObj.SetFormalCharge(charge)
        AtomObj.SetNumRadicalElectrons(radical)
        mol.AddAtom(AtomObj)
        radicalType += radical

    for start_idx, end_idx, bond_type in bonds:
        mol.AddBond(start_idx, end_idx, BondOrders[bond_type])

    Charge = Chem.GetFormalCharge(mol)

    Chem.SanitizeMol(mol)
    mol = Chem.RemoveHs(mol)
    SMILES = Chem.MolToSmiles(mol)

    return SMILES, radicalType


def processEntry(entry):
    try:
        (idx,
         atoms, bonds,
         formal_charges,
         formal_num_radicals) = [ast.literal_eval(fomatter(str(item))) for item in entry]
        #formal_num_radicals = ast.literal_eval(formal_num_radicals)
        charge = sum(formal_charges)
        SMILES, radicalType = createSmiles(atoms, bonds, formal_charges, formal_num_radicals)
        return idx, SMILES, radicalType
    except:
        return entry[0], None, 999

total_saved = 0

if __name__ == '__main__':
    with open(final_csv, 'w') as f:
        f.write("HF,SMILES,Radical Type\n")

    for chunkNum, chunk in enumerate(pd.read_csv(csv, chunksize=chunk_size)):
        print("processing chunk :", chunkNum, "/ 40")

        entrys = list(zip(chunk.index, chunk["atoms"], chunk["bonds"], chunk["formal_charges"], chunk["formal_num_radicals"]))

        smilesResults = {}
        radicalResults = {}
        with ProcessPoolExecutor(max_workers=num_cores, initializer=init_worker) as executor:
            for idx, smiles, radicalType in executor.map(processEntry, entrys, chunksize=500):
                if radicalType <= 2: # drop anything bigger becuase not needed for the algorthim
                    smilesResults[idx] = smiles
                    radicalResults[idx] = radicalType

        chunk['SMILES'] = chunk.index.map(smilesResults)
        chunk['Radical Type'] = chunk.index.map(radicalResults)
        chunk_clean = chunk.drop(columns=["bonds", "atoms", "formal_charges", "formal_num_radicals"])
        chunk_clean = chunk_clean.dropna(subset=["SMILES"])

        total_saved += len(chunk_clean)
        print(f" -> Successfully appended {len(chunk_clean)} rows. Cumulative total: {total_saved}")

        # Save without wiping old progress or stacking duplicate headers
        chunk_clean.to_csv(final_csv, index=False, mode='a', header=False)