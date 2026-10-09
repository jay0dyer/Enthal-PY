import rdkit
import sqlite3

class EnthalpyMolecule:
    def __init__(self, Smiles):
        self.conn = sqlite3.connect("Database/Temp/EnthalpyTables.db")
        self.Smiles = Smiles
        self.cursor = self.conn.cursor()

    def SreachFragmentEnthalpy(self, fragmentSmiles):
        self.cursor.execute("SELECT * FROM Radical_0 WHERE SMILES = ?", (fragmentSmiles,))
        return self.cursor.fetchall()

    def RBS(self):



testmol = EnthalpyMolecule()