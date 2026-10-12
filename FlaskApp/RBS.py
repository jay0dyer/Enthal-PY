import rdkit
from rdkit import Chem
import sqlite3

class EnthalpyMolecule:
    def __init__(self, Smiles):
        self.mol = Chem.MolFromSmiles(Smiles)
        self.conn = sqlite3.connect("Database/Temp/EnthalpyTables.db")
        self.Smiles = Smiles
        self.cursor = self.conn.cursor()

    def SearchFragmentEnthalpyBySMILES(self, fragmentSmiles):
        print("SearchFragmentEnthalpyBySMILES : searching for", fragmentSmiles, end=" ")
        self.cursor.execute("SELECT * FROM Radical_0 WHERE SMILES = ?", (fragmentSmiles,))
        result = self.cursor.fetchall()
        if len(result) != 0:
            print("Enthalpy found", result[0][1])
            return result[0][1]
        else:
            raise Exception(f"SMILES : {fragmentSmiles} not found in database")

    def SearchFragmentEnthalpy(self, mol):
        canonical_smiles = Chem.MolToSmiles(mol)
        return self.SearchFragmentEnthalpyBySMILES(canonical_smiles)


    def RBS(self):
        pass

    def FindBondEnthalpy(self, fragmentA, fragmentB, SubMolecule):
        bondEnthalpy =  self.SearchFragmentEnthalpy(SubMolecule) - (self.SearchFragmentEnthalpy(fragmentA) + self.SearchFragmentEnthalpy(fragmentB))
        return bondEnthalpy



testmol = EnthalpyMolecule("CC")

A = Chem.MolFromSmiles("CO")
B = Chem.MolFromSmiles("C")
SubMol = Chem.MolFromSmiles("CCO")
print("enthalpy for bond C-CO is ", testmol.FindBondEnthalpy(A, B, SubMol))