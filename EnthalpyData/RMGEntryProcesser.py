class RequiredDataEntry():
    def __init__(self, index, label, molecule, thermo, reference, **kwargs):
        SMILES = self.SMILESLabelProcesser(label)
        if SMILES == None:
            SMILES = self.SMILESMoleculeProcesser(label)

        self.SMILES = SMILES
        self.molecule = molecule
        self.thermo = thermo
        self.reference = reference
        #print(thermo)

    def IsVaildSmiles(self, SMILES):
        return True

    def FixForRDKIT(self, SMILES):
        # the main issue is that some of the SMILES contain D for dueterium
        # RDKIT dosent handle this so at the risk of loss of some accuacry it can be treated as hydrogen
        RDKITSMILES = SMILES
        return RDKITSMILES

    def FromMolecule(self, molecule):
        return molecule

    def SMILESLabelProcesser(self, preSMILES):
        SMILES = self.FixForRDKIT(preSMILES)
        if self.IsVaildSmiles(SMILES):
            return SMILES
        else:
            return None

    def SMILESMoleculeProcesser(self, molecule):
        SMILES = self.FromMolecule(molecule)
        if self.IsVaildSmiles(SMILES):
            return SMILES
        else:
            return None

    def returnInfo(self):
        return self.SMILES, self.thermo, self.reference