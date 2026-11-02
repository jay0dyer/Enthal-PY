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
        self.FindFragmentsInSub(self.mol)

    def removeDummyAtom(self, mol):
        bondTypeHomolyticLookUp = {
            "SINGLE" : 1,
            "DOUBLE" : 2,
            "TRIPLE" : 3
        }

        rw_mol = Chem.RWMol(mol)
        dummy_idxs = [atom.GetIdx() for atom in rw_mol.GetAtoms() if atom.GetAtomicNum() == 0]
        dummy_atoms = [rw_mol.GetAtomWithIdx(dummy_idx) for dummy_idx in dummy_idxs]

        rw_mol.BeginBatchEdit() # stops index changing when atoms are removed as there removed in batchs

        for dummy_atom, dummy_idx in zip(dummy_atoms, dummy_idxs):
            for neighbor in dummy_atom.GetNeighbors():
                bond = rw_mol.GetBondBetweenAtoms(dummy_idx, neighbor.GetIdx())
                bondType = str(bond.GetBondType()) # gets bond type to reffence for radical state
                neighbor.SetNumRadicalElectrons(bondTypeHomolyticLookUp[bondType])
                rw_mol.RemoveAtom(dummy_idx)
        rw_mol.CommitBatchEdit()

        Chem.SanitizeMol(rw_mol)

        return rw_mol

    def FindFragmentsInSub(self, submol):
        size = submol.GetNumAtoms()
        index = round(size / 2)
        print(index)
        bondType = submol.GetBonds()[index].GetBondType()
        mol_frag = Chem.FragmentOnBonds(submol, (index,), bondTypes=[bondType])
        fragments = Chem.GetMolFrags(mol_frag, asMols=True)

        for i, frag in enumerate(fragments):
            frag = self.removeDummyAtom(frag)
            print("fragment :",Chem.MolToSmiles(frag))



EnthalpyMol = EnthalpyMolecule("C=C=C=C")
EnthalpyMol.RBS()