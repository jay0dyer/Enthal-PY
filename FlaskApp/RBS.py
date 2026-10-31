from EnthalpySearch import EnthalpySearch
import rdkit
from rdkit import Chem
from rdkit.Chem import AllChem

class EnthalpyMolecule(EnthalpySearch):
    def __init__(self, Smiles):
        super().__init__() # calls the search engines init .. bruv
        self.mol = Chem.MolFromSmiles(Smiles)
        Chem.Kekulize(self.mol, clearAromaticFlags=True)

    def RBS(self):
        pass

    def removeDummyAtom(self, mol):
        bondTypeHomolyticLookUp = {
            "SINGLE" : 1,
            "DOUBLE" : 2,
            "TRIPLE" : 3
        }

        rw_mol = Chem.RWMol(mol)
        dummy_idx = [atom.GetIdx() for atom in rw_mol.GetAtoms() if atom.GetAtomicNum() == 0][0]
        dummy_atom = rw_mol.GetAtomWithIdx(dummy_idx)

        for neighbor in dummy_atom.GetNeighbors():
            bond = rw_mol.GetBondBetweenAtoms(dummy_idx, neighbor.GetIdx())
            bondType = str(bond.GetBondType())
            neighbor.SetNumRadicalElectrons(bondTypeHomolyticLookUp[bondType])

        # 5. Remove the dummy atom
        rw_mol.RemoveAtom(dummy_idx)

        Chem.SanitizeMol(rw_mol)

        return rw_mol

    def FindFragments(self, index):
        bondType = self.mol.GetBonds()[index].GetBondType()
        mol_frag = Chem.FragmentOnBonds(self.mol, (index,), bondTypes=[bondType])
        fragments = Chem.GetMolFrags(mol_frag, asMols=True)

        for i, frag in enumerate(fragments):
            frag = self.removeDummyAtom(frag)
            print("fragment :",Chem.MolToSmiles(frag))
            




EnthalpyMol = EnthalpyMolecule("c1ccccc1")
EnthalpyMol.FindFragments(0)