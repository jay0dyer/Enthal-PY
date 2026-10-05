from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Draw

def DisplaySmiles():
    mol = Chem.MolFromSmiles("N#N.[H]C(=O)N=C=O")
    img = Draw.MolToImage(m)
    with open("static/images/currentmolview.png", "wb") as file_out:
        file_out

