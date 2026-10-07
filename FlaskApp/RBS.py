import rdkit
import sqlite3

class EnthalpyMolecule:
    def __init__(self):
        self.conn = sqlite3.connect("Database/Temp/EnthalpyTables.db")
        self.cursor = self.conn.cursor()

    def SreachFragmentEnthalpy(self, fragmentSmiles):
        self.cursor.execute("SELECT * FROM Radical_0 WHERE SMILES = ?", (fragmentSmiles,))
        return self.cursor.fetchall()

    def bondEnthalpy(self):

testmol = EnthalpyMolecule()