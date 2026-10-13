from EnthalpySearch import EnthalpySearch
import rdkit
from rdkit import Chem

class EnthalpyMolecule:
    def __init__(self, Smiles):
        self.mol = Chem.MolFromSmiles(Smiles)

    def FindBondEnthalpy(self, fragmentA, fragmentB, SubMolecule):
        bondEnthalpy = (self.SearchMolEnthalpy(SubMolecule) -
                        (self.SearchMolEnthalpy(fragmentA) + self.SearchMolEnthalpy(fragmentB)))
        return bondEnthalpy

    def RBS(self):
        pass



engine = EnthalpySearch()

SubMol = Chem.MolFromSmiles("C1CC1C2CC2")
A = Chem.MolFromSmiles("OCC[CH2]")
B = Chem.MolFromSmiles("OCC[CH2]")
print("enthalpy for bond OCCCCCCO is ", engine.FindBondEnthalpy(A, B, SubMol))