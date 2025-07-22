#!/usr/bin/env python3
"""
Example usage of the PubChem SMILES retrieval function.
"""

from get_cancer_drugs import get_smiles_from_pubchem
import pandas as pd

def main():
    # Example 1: Simple drug list
    print("Example 1: Querying SMILES for common drugs")
    print("=" * 50)
    
    drug_list = [
        "aspirin",
        "ibuprofen", 
        "acetaminophen",
        "caffeine",
        "morphine",
        "invalid_drug_xyz"  # This should return N/A
    ]
    
    # Get SMILES strings
    results_df = get_smiles_from_pubchem(drug_list)
    
    # Display results
    print("\nResults:")
    print(results_df.to_string(index=False))
    
    # Save to CSV
    results_df.to_csv('example_drug_smiles.csv', index=False)
    print(f"\nResults saved to 'example_drug_smiles.csv'")
    
    # Example 2: Show how to filter out N/A results
    print("\n" + "=" * 50)
    print("Example 2: Filtering out drugs not found in PubChem")
    
    # Filter out N/A results
    found_drugs = results_df[results_df['SMILES'] != 'N/A']
    not_found_drugs = results_df[results_df['SMILES'] == 'N/A']
    
    print(f"\nDrugs found in PubChem ({len(found_drugs)}):")
    print(found_drugs.to_string(index=False))
    
    print(f"\nDrugs NOT found in PubChem ({len(not_found_drugs)}):")
    print(not_found_drugs[['Drug Name']].to_string(index=False))
    
    # Example 3: Basic statistics
    print("\n" + "=" * 50)
    print("Example 3: Basic statistics")
    
    total_drugs = len(results_df)
    found_count = len(found_drugs)
    not_found_count = len(not_found_drugs)
    success_rate = (found_count / total_drugs) * 100 if total_drugs > 0 else 0
    
    print(f"\nTotal drugs queried: {total_drugs}")
    print(f"Found in PubChem: {found_count}")
    print(f"Not found: {not_found_count}")
    print(f"Success rate: {success_rate:.1f}%")
    
    # Example 4: SMILES length analysis
    if len(found_drugs) > 0:
        print("\n" + "=" * 50)
        print("Example 4: SMILES string length analysis")
        
        found_drugs['SMILES_Length'] = found_drugs['SMILES'].str.len()
        
        print(f"\nSMILES length statistics:")
        print(f"Average length: {found_drugs['SMILES_Length'].mean():.1f}")
        print(f"Min length: {found_drugs['SMILES_Length'].min()}")
        print(f"Max length: {found_drugs['SMILES_Length'].max()}")
        
        print(f"\nShortest SMILES:")
        shortest_idx = found_drugs['SMILES_Length'].idxmin()
        print(f"{found_drugs.loc[shortest_idx, 'Drug Name']}: {found_drugs.loc[shortest_idx, 'SMILES']}")
        
        print(f"\nLongest SMILES:")
        longest_idx = found_drugs['SMILES_Length'].idxmax()
        print(f"{found_drugs.loc[longest_idx, 'Drug Name']}: {found_drugs.loc[longest_idx, 'SMILES']}")

if __name__ == "__main__":
    main()