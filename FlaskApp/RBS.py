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

SubMol = Chem.MolFromSmiles("[C]=C1O[C+]1OCCCO")
A = Chem.MolFromSmiles("[C]=C1O[C+]1OC[CH2]")
B = Chem.MolFromSmiles("[CH2]O")
print("enthalpy for bond N#N is ", engine.FindBondEnthalpy(A, B, SubMol))