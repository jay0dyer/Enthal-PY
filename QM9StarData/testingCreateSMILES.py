import pandas as pd
from rdkit import Chem

fomatter = lambda text : text.translate(str.maketrans({"{":"[","}":"]"})).replace("nan","None")
BondOrders = {1:Chem.BondType.SINGLE, 2:Chem.BondType.DOUBLE, 3:Chem.BondType.TRIPLE, 12:Chem.BondType.AROMATIC}

def createSmiles(atoms, bonds, formal_charges):
    mol = Chem.RWMol()
    for atom, charge in zip(atoms, formal_charges):
        AtomObj = Chem.Atom(atom)
        AtomObj.SetFormalCharge(charge)
        mol.AddAtom(AtomObj)

    for start_idx, end_idx, bond_type in bonds:
        mol.AddBond(start_idx, end_idx, BondOrders[bond_type])

    Charge = Chem.GetFormalCharge(mol)

    mol = Chem.RemoveHs(mol)
    Chem.SanitizeMol(mol)
    SMILES = Chem.MolToSmiles(mol)

    return SMILES, Charge

def processEntry(entry):
    (idx,
     atoms, bonds,
     formal_charges) = [eval(fomatter(str(item))) for item in entry][:4]
    #formal_num_radicals = ast.literal_eval(formal_num_radicals)
    SMILES, Charge = createSmiles(atoms, bonds, formal_charges)
    return idx, SMILES, Charge

csv = pd.read_csv("qm9star_practice_raw.csv")
entrys = list(zip(csv.index, csv['atoms'], csv['bonds'], csv['formal_charges'], csv['H_T']))
for entry in entrys:
    processed = processEntry(entry)
    if processed[2] > 0:
        print(processed)