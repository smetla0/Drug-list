# PubChem SMILES Retrieval Tool

This Python tool queries the PubChem database to retrieve SMILES (Simplified Molecular Input Line Entry System) strings for drug names.

## Features

- Query PubChem REST API for drug compound information
- Retrieve SMILES strings for a list of drug names
- Return results in a pandas DataFrame format
- Handle missing/not found drugs by marking them as "N/A"
- Respectful API usage with configurable delays between requests
- Support for different SMILES formats (Canonical, Isomeric, Connectivity)

## Installation

```bash
pip install -r requirements.txt
```

Or install packages individually:
```bash
pip install pandas requests
```

## Usage

### Basic Usage

```python
from get_cancer_drugs import get_smiles_from_pubchem

# List of drug names
drug_names = ["aspirin", "ibuprofen", "caffeine", "morphine"]

# Get SMILES strings
df = get_smiles_from_pubchem(drug_names)

print(df)
```

### Example Output

```
   Drug Name                        SMILES
     aspirin      CC(=O)OC1=CC=CC=C1C(=O)O
   ibuprofen CC(C)CC1=CC=C(C=C1)C(C)C(=O)O
    caffeine  CN1C=NC2=C1C(=O)N(C(=O)N2C)C
    morphine CN1CC[C@]23[C@@H]4[C@H]1CC5=...
```

### Loading from CSV

```python
from get_cancer_drugs import load_drug_names_from_csv, get_smiles_from_pubchem

# Load drug names from CSV file
drug_names = load_drug_names_from_csv('your_drugs.csv', 'drug_name_column')

# Get SMILES strings
df = get_smiles_from_pubchem(drug_names)

# Save results
df.to_csv('drug_smiles_results.csv', index=False)
```

### Function Parameters

- `drug_names`: List of drug names to query
- `delay`: Delay between API calls in seconds (default: 0.2s)

## Files

- `get_cancer_drugs.py`: Main module with SMILES retrieval functions
- `example_usage.py`: Example usage with statistics and analysis
- `requirements.txt`: Required Python packages
- `README.md`: This documentation file

## API Rate Limiting

The tool includes a configurable delay between API requests (default 0.2 seconds) to be respectful to the PubChem servers. You can adjust this delay based on your needs:

```python
# Faster queries (use with caution)
df = get_smiles_from_pubchem(drug_names, delay=0.1)

# Slower, more conservative queries
df = get_smiles_from_pubchem(drug_names, delay=0.5)
```

## Error Handling

- Network errors are caught and logged
- Drugs not found in PubChem are marked as "N/A"
- Invalid responses are handled gracefully
- Progress is displayed during processing

## Example Run

Run the example to see the tool in action:

```bash
python3 example_usage.py
```

This will:
1. Query SMILES for common drugs
2. Show filtering examples
3. Display basic statistics
4. Analyze SMILES string lengths

## Notes

- The tool queries PubChem's REST API which is free and publicly available
- Some drug names (especially brand names or very new drugs) may not be found
- Large biological molecules (proteins, antibodies) typically don't have SMILES representations
- SMILES strings represent the chemical structure and can be used for further molecular analysis

## Dependencies

- pandas: For DataFrame operations
- requests: For HTTP API calls
- urllib.parse: For URL encoding (built-in Python module)