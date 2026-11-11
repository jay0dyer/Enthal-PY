import rdkit
from rdkit import Chem
from rdkit.Chem import Descriptors
import sqlite3

class EnthalpySearch:
    def __init__(self):
        self.conn = sqlite3.connect("Database/Temp/EnthalpyTables.db")
        self.cursor = self.conn.cursor()

    def SearchRadicalsBySMILES(self, SubMolSmiles, charge, mute=True):
        if not mute:
            print("SearchRadicalsBySMILES : searching for", SubMolSmiles, f"in Radical_{charge}", end=" ")
        self.cursor.execute(f"SELECT * FROM Radical_{charge} WHERE SMILES = ?", (SubMolSmiles,))
        result = self.cursor.fetchall()
        if len(result) != 0:
            if not mute:
                print("Enthalpy found", result[0][1])
            return result[0][1]
        else:
            print("Enthalpy not found")
            raise Exception(f"SMILES : {SubMolSmiles} not found in Radical_{charge}")

    def SearchMolEnthalpy(self, mol):
        Charge = Descriptors.NumRadicalElectrons(mol)
        canonical_smiles = Chem.MolToSmiles(mol)
        return self.SearchRadicalsBySMILES(canonical_smiles, Charge)

if __name__ == "__main__":
    engine = EnthalpySearch()
    SubMol = Chem.MolFromSmiles("CC")
    engine.SearchMolEnthalpy(SubMol)

