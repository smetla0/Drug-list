import pandas as pd
import requests
import time
from typing import List, Dict, Optional
import urllib.parse


def get_smiles_from_pubchem(drug_names: List[str], delay: float = 0.2) -> pd.DataFrame:
    """
    Query PubChem to get SMILES strings for a list of drug names.
    
    Args:
        drug_names: List of drug names to query
        delay: Delay between API calls in seconds (default 0.2s to be respectful to PubChem)
    
    Returns:
        pandas DataFrame with columns 'Drug Name' and 'SMILES'
    """
    results = []
    
    for i, drug_name in enumerate(drug_names):
        print(f"Processing {i+1}/{len(drug_names)}: {drug_name}")
        
        smiles = query_pubchem_for_smiles(drug_name)
        results.append({
            'Drug Name': drug_name,
            'SMILES': smiles if smiles else 'N/A'
        })
        
        # Add delay to be respectful to PubChem API
        if i < len(drug_names) - 1:  # Don't delay after the last request
            time.sleep(delay)
    
    return pd.DataFrame(results)


def query_pubchem_for_smiles(drug_name: str) -> Optional[str]:
    """
    Query PubChem for a single drug name and return its SMILES string.
    
    Args:
        drug_name: Name of the drug to query
        
    Returns:
        SMILES string if found, None otherwise
    """
    try:
        # First, try to get the compound ID (CID) using the name
        search_url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/{urllib.parse.quote(drug_name)}/cids/JSON"
        
        response = requests.get(search_url, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        
        if 'IdentifierList' not in data or 'CID' not in data['IdentifierList']:
            return None
            
        # Get the first CID
        cid = data['IdentifierList']['CID'][0]
        
        # Now get the SMILES using the CID
        smiles_url = f"https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/{cid}/property/CanonicalSMILES,IsomericSMILES/JSON"
        
        response = requests.get(smiles_url, timeout=10)
        response.raise_for_status()
        
        smiles_data = response.json()
        
        if 'PropertyTable' in smiles_data and 'Properties' in smiles_data['PropertyTable']:
            properties = smiles_data['PropertyTable']['Properties']
            if properties:
                # Try different SMILES properties in order of preference
                for smiles_key in ['CanonicalSMILES', 'IsomericSMILES', 'SMILES', 'ConnectivitySMILES']:
                    if smiles_key in properties[0]:
                        return properties[0][smiles_key]
        
        return None
        
    except requests.exceptions.RequestException as e:
        print(f"Request error for {drug_name}: {e}")
        return None
    except Exception as e:
        print(f"Error processing {drug_name}: {e}")
        return None


def load_drug_names_from_csv(csv_file: str, column_name: str = 'drug_name') -> List[str]:
    """
    Load drug names from a CSV file.
    
    Args:
        csv_file: Path to the CSV file
        column_name: Name of the column containing drug names
        
    Returns:
        List of drug names
    """
    try:
        df = pd.read_csv(csv_file)
        if column_name not in df.columns:
            print(f"Column '{column_name}' not found. Available columns: {list(df.columns)}")
            return []
        return df[column_name].dropna().tolist()
    except Exception as e:
        print(f"Error loading CSV file: {e}")
        return []


def main():
    """
    Example usage of the function.
    """
    # Example with a small list of drug names
    sample_drugs = [
        "aspirin",
        "ibuprofen", 
        "acetaminophen",
        "caffeine",
        "invalid_drug_name_xyz123"
    ]
    
    print("Testing with sample drug names...")
    df = get_smiles_from_pubchem(sample_drugs)
    print("\nResults:")
    print(df.to_string(index=False))
    
    # Save results to CSV
    df.to_csv('drug_smiles_results.csv', index=False)
    print(f"\nResults saved to 'drug_smiles_results.csv'")
    
    # Example with loading from the cancer drugs CSV file
    print("\n" + "="*50)
    print("Loading drug names from cancer_drugs.csv...")
    
    # First, let's check what columns are available in the CSV
    try:
        sample_df = pd.read_csv('cancer_drugs.csv', nrows=5)
        print(f"Available columns in cancer_drugs.csv: {list(sample_df.columns)}")
        print("First few rows:")
        print(sample_df.head())
        
        # Try to identify the drug name column
        drug_column = None
        for col in sample_df.columns:
            if any(keyword in col.lower() for keyword in ['drug', 'name', 'compound', 'medication']):
                drug_column = col
                break
        
        if drug_column:
            print(f"\nUsing column '{drug_column}' for drug names")
            drug_names = load_drug_names_from_csv('cancer_drugs.csv', drug_column)
            
            # Process only the first 10 drugs as an example
            if drug_names:
                print(f"Found {len(drug_names)} drug names. Processing first 10...")
                sample_cancer_drugs = drug_names[:10]
                cancer_df = get_smiles_from_pubchem(sample_cancer_drugs)
                print("\nResults for cancer drugs:")
                print(cancer_df.to_string(index=False))
                cancer_df.to_csv('cancer_drug_smiles_sample.csv', index=False)
                print("Sample results saved to 'cancer_drug_smiles_sample.csv'")
        else:
            print("Could not automatically identify drug name column")
            
    except Exception as e:
        print(f"Error processing cancer_drugs.csv: {e}")


if __name__ == "__main__":
    main()
