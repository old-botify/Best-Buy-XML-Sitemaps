import os
import pandas as pd
from pathlib import Path

def combine_csvs(folder_path):
    # Convert folder path to Path object
    folder = Path(folder_path)
    
    # List to store all dataframes
    dfs = []
    
    # Iterate through all CSV files in the folder
    for csv_file in folder.glob('*.csv'):
        try:
            # Read the file content
            with open(csv_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            # Remove 'sep=,' if it exists at the start
            if lines and lines[0].strip() == 'sep=,':
                lines = lines[1:]
            
            # Write cleaned content to a temporary string
            from io import StringIO
            cleaned_content = StringIO(''.join(lines))
            
            # Read the cleaned CSV content
            df = pd.read_csv(cleaned_content)
            
            # Add source file column for tracking
            df['source_file'] = csv_file.name
            
            dfs.append(df)
            print(f"Successfully processed: {csv_file.name}")
            
        except Exception as e:
            print(f"Error processing {csv_file.name}: {str(e)}")
    
    if not dfs:
        raise ValueError("No CSV files were successfully processed")
    
    # Combine all dataframes
    combined_df = pd.concat(dfs, ignore_index=True)
    
    # Remove duplicates based on all columns except the source_file
    columns_for_dedup = [col for col in combined_df.columns if col != 'source_file']
    combined_df = combined_df.drop_duplicates(subset=columns_for_dedup, keep='first')
    
    return combined_df

def main():
    # Folder path containing the CSV files
    folder_path = "botify_export"
    
    try:
        # Combine CSVs
        print(f"\nProcessing CSV files in folder: {folder_path}")
        combined_df = combine_csvs(folder_path)
        
        # Generate output filename
        output_file = "combined_botify_export.csv"
        
        # Save the combined CSV
        combined_df.to_csv(output_file, index=False)
        
        # Print summary statistics
        print(f"\nSummary:")
        print(f"Total rows in combined file: {len(combined_df)}")
        print(f"Number of unique URLs: {combined_df['Full URL'].nunique()}")
        print(f"Source files processed: {combined_df['source_file'].nunique()}")
        print(f"\nOutput saved to: {output_file}")
        
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()