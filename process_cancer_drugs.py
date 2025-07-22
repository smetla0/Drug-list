#!/usr/bin/env python3
"""
Script to process all cancer drugs from cancer_drugs.csv and get their SMILES strings.
"""

import pandas as pd
from get_cancer_drugs import get_smiles_from_pubchem, load_drug_names_from_csv

def main():
    # Load drug names from the CSV file
    print("Loading drug names from cancer_drugs.csv...")
    drug_names = load_drug_names_from_csv('cancer_drugs.csv')
    print(f'Found {len(drug_names)} drugs in cancer_drugs.csv')
    
    if len(drug_names) == 0:
        print("No drug names found. Exiting.")
        return
    
    # Get SMILES strings for all drugs
    print('Starting SMILES retrieval...')
    print('This may take a while due to API rate limiting...')
    results_df = get_smiles_from_pubchem(drug_names, delay=0.3)
    
    # Save results to a new CSV file
    output_file = 'cancer_drugs_with_smiles.csv'
    results_df.to_csv(output_file, index=False)
    print(f'\nResults saved to {output_file}')
    
    # Show summary statistics
    total_drugs = len(results_df)
    found_smiles = len(results_df[results_df['SMILES'] != 'N/A'])
    not_found = total_drugs - found_smiles
    
    print(f'\nSummary:')
    print(f'Total drugs processed: {total_drugs}')
    print(f'SMILES found: {found_smiles} ({found_smiles/total_drugs*100:.1f}%)')
    print(f'SMILES not found: {not_found} ({not_found/total_drugs*100:.1f}%)')
    
    # Show first few results
    print(f'\nFirst 10 results:')
    print(results_df.head(10).to_string(index=False))
    
    # Show some examples of drugs that were found and not found
    found_drugs = results_df[results_df['SMILES'] != 'N/A']
    not_found_drugs = results_df[results_df['SMILES'] == 'N/A']
    
    if len(found_drugs) > 0:
        print(f'\nExample drugs with SMILES found:')
        print(found_drugs.head(5)[['Drug Name', 'SMILES']].to_string(index=False))
    
    if len(not_found_drugs) > 0:
        print(f'\nExample drugs with SMILES not found:')
        print(not_found_drugs.head(5)['Drug Name'].to_string(index=False))

if __name__ == "__main__":
    main()