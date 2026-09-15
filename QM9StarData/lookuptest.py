import pandas as pd
from rdkit import Chem

star = pd.read_csv('DATA/SMILESEnthalpyLookUp.csv')
og = pd.read_csv('DATA/qm9.csv')

print(star.info())
print(og.info())