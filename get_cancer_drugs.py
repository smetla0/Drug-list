import pandas as pd
from rdkit import Chem

# Step 1: Load your drug data from a CSV
df = pd.read_csv("approved_drugs.csv")  # Make sure you have this CSV!

# Step 2: Filter only cancer-related drugs
cancer_drugs = df[df["Indication"].str.contains("cancer|tumor|oncology|neoplasm", case=False, na=False)]

# Step 3: Check if SMILES are valid
cancer_drugs["mol"] = cancer_drugs["SMILES"].apply(Chem.MolFromSmiles)
valid_cancer_drugs = cancer_drugs[cancer_drugs["mol"].notnull()]

# Step 4: Print the first few results
print(valid_cancer_drugs[["Drug Name", "SMILES"]].head())
