from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Draw

def DisplaySmiles(Smiles):
    mol = Chem.MolFromSmiles(Smiles)
    img = Draw.MolToImage(m)
    with open("static/images/currentmolview.png", "wb") as file_out:
        file_out

