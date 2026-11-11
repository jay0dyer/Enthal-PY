from logging import exception

from EnthalpySearch import EnthalpySearch
from rdkit import Chem
import MolViewer

class EnthalpyMolecule(EnthalpySearch):
    def __init__(self, Smiles):
        super().__init__() # calls the search engines init .. bruv
        self.Smiles = Smiles
        self.mol = Chem.MolFromSmiles(Smiles)
        Chem.Kekulize(self.mol, clearAromaticFlags=True)

        self.EnthalpyMapMol = self.BabyRBS()

    def RBS(self):
        pass

    def BabyRBS(self): # RBS where the sub mol is allways two atoms
        EnthalpyMapMol = Chem.AddHs(self.mol)
        for bond in EnthalpyMapMol.GetBonds():
            bondtype = bond.GetBondType()
            submol = Chem.RWMol()
            atom1 = bond.GetBeginAtom()
            atom2 = bond.GetEndAtom()

            submol.AddAtom(atom1)
            submol.AddAtom(atom2)

            #print("-"*30)

            submol.AddBond(0, 1, bondtype)
            Chem.SanitizeMol(submol)
            #print("Checking bond :",Chem.MolToSmiles(submol))

            bond_idx = self.findBondIdx(submol)
            submol, halfs = self.FindFragmentsInSub(submol, bond_idx)
            #print("Sreaching for fragments :")
            #for fragment in halfs:
                #print(Chem.MolToSmiles(fragment))

            Enthalpy = (sum([self.SearchMolEnthalpy(half) for half in halfs]) - self.SearchMolEnthalpy(submol))
            bond.SetDoubleProp("Enthalpy", Enthalpy)
        return EnthalpyMapMol

    def FindBondEnthalpy(self, fragments, SubMolecule):
        bondEnthalpy = (self.SearchMolEnthalpy(SubMolecule) -
                        sum([self.SearchMolEnthalpy(fragment) for fragment in fragments]))
        return bondEnthalpy

    def findBondIdx(self, submol):
        bonds_to_break = [bond.GetIdx() for bond in submol.GetBonds()
                          if bond.GetBeginAtom().GetAtomicNum() > 1 and bond.GetEndAtom().GetAtomicNum() > 1]

        if not bonds_to_break:
            bonds_to_break = [bond.GetIdx() for bond in submol.GetBonds()
                              if (bond.GetBeginAtom().GetAtomicNum() > 1 and bond.GetEndAtom().GetAtomicNum() == 1) or
                              (bond.GetBeginAtom().GetAtomicNum() == 1 and bond.GetEndAtom().GetAtomicNum() > 1)]

        if not bonds_to_break:
            bonds_to_break = [bond.GetIdx() for bond in submol.GetBonds()]

        if not bonds_to_break:
            return Chem.RemoveHs(submol), []

        bond_idx = bonds_to_break[len(bonds_to_break) // 2]

        return bond_idx

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

    def FindFragmentsInSub(self, submol, bond_idx):
        bondType = submol.GetBonds()[bond_idx].GetBondType()
        mol_frag = Chem.FragmentOnBonds(submol, (bond_idx,), bondTypes=[bondType])
        fragments = list(Chem.GetMolFrags(mol_frag, asMols=True))

        # removes impliecnt hydrogens for use in sreaching the DB
        fragments = [Chem.RemoveHs(fragment, updateExplicitCount=True) for fragment in fragments]

        for i, frag in enumerate(fragments):
            fragments[i] = self.removeDummyAtom(frag)

        submol = Chem.RemoveHs(submol)
        return submol, fragments




moleculesmiles = [
    "[FH]",
]

s = 0
for smiles in moleculesmiles:
    EnthalpyMol = EnthalpyMolecule(smiles)
    EnthalpyMol.BabyRBS()
    MolViewer.DisplayMolA(EnthalpyMol)
