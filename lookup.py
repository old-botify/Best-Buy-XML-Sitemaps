import pandas as pd
from tqdm import tqdm
import os

def process_urls_and_sitemaps(botify_file, urls_file, output_dir='./output'):
    """
    Process URLs and sitemaps from two CSV files, joining datasets and analyzing indexability
    
    Args:
        botify_file (str): Path to the Botify CSV file with status codes and indexability
        urls_file (str): Path to the URLs file containing XML sitemap data
        output_dir (str): Directory for output files
    """
    print("Loading data files...")
    
    # Read the CSVs with progress bars
    with tqdm(total=2, desc="Reading CSV files") as pbar:
        botify_df = pd.read_csv(botify_file)
        pbar.update(1)
        sitemap_df = pd.read_csv(urls_file)
        pbar.update(1)
    
    print("\nProcessing URLs and generating reports...")
    
    # Create a mapping of URL to source sitemaps (handling multiple sitemaps per URL)
    with tqdm(total=1, desc="Creating sitemap mapping") as pbar:
        sitemap_mapping = sitemap_df.groupby('URL')['Source Sitemap'].agg(lambda x: ','.join(x.unique())).reset_index()
        sitemap_mapping.columns = ['Full URL', 'Source Sitemaps']
        pbar.update(1)
    
    # Merge Botify data with sitemap data
    with tqdm(total=1, desc="Merging datasets") as pbar:
        # Left join to keep all Botify URLs and add sitemap information where available
        merged_df = pd.merge(botify_df, sitemap_mapping, on='Full URL', how='left')
        pbar.update(1)
    
    # Analyze URLs and create reports
    with tqdm(total=4, desc="Analyzing URLs") as pbar:
        # URLs in sitemaps that are non-indexable (should be removed)
        sitemap_urls_to_remove = merged_df[
            (merged_df['Source Sitemaps'].notna()) & 
            (merged_df['Non-Indexable Main Reason'].notna())
        ].copy()
        pbar.update(1)
        
        # URLs in sitemaps that are indexable (good to keep)
        sitemap_urls_valid = merged_df[
            (merged_df['Source Sitemaps'].notna()) & 
            (merged_df['Non-Indexable Main Reason'].isna())
        ].copy()
        pbar.update(1)
        
        # URLs not in sitemaps but are indexable (potential additions)
        missing_indexable_urls = merged_df[
            (merged_df['Source Sitemaps'].isna()) & 
            (merged_df['Non-Indexable Main Reason'].isna())
        ].copy()
        pbar.update(1)
        
        # Create pagetype analysis
        pagetype_analysis = merged_df.groupby(['pagetype', 'Non-Indexable Main Reason']).size().reset_index(name='count')
        pagetype_analysis = pagetype_analysis.sort_values(['pagetype', 'count'], ascending=[True, False])
        pbar.update(1)
    
    # Save outputs
    print("\nSaving output files...")
    os.makedirs(output_dir, exist_ok=True)
    
    with tqdm(total=6, desc="Writing files") as pbar:
        # Save complete dataset
        merged_df.to_csv(f'{output_dir}/complete_dataset.csv', index=False)
        pbar.update(1)
        
        # Save URLs to remove from sitemaps
        sitemap_urls_to_remove.to_csv(f'{output_dir}/urls_to_remove_from_sitemap.csv', index=False)
        pbar.update(1)
        
        # Save valid sitemap URLs
        sitemap_urls_valid.to_csv(f'{output_dir}/valid_sitemap_urls.csv', index=False)
        pbar.update(1)
        
        # Save potentially missing URLs
        missing_indexable_urls.to_csv(f'{output_dir}/missing_indexable_urls.csv', index=False)
        pbar.update(1)
        
        # Save pagetype analysis
        pagetype_analysis.to_csv(f'{output_dir}/pagetype_analysis.csv', index=False)
        pbar.update(1)
        
        # Save sitemap-specific analysis
        sitemap_analysis = merged_df[merged_df['Source Sitemaps'].notna()].groupby('Source Sitemaps')[['Non-Indexable Main Reason']].value_counts().reset_index(name='count')
        sitemap_analysis.to_csv(f'{output_dir}/sitemap_analysis.csv', index=False)
        pbar.update(1)
    
    # Print summary statistics
    print("\nProcessing complete! Summary:")
    print(f"Total URLs in Botify export: {len(botify_df)}")
    print(f"Total URLs in XML sitemaps: {len(sitemap_df)}")
    print(f"URLs in sitemaps that should be removed (non-indexable): {len(sitemap_urls_to_remove)}")
    print(f"Valid URLs in sitemaps: {len(sitemap_urls_valid)}")
    print(f"Indexable URLs not in sitemaps: {len(missing_indexable_urls)}")
    
    print("\nPagetype Analysis Preview:")
    pd.set_option('display.max_rows', 20)
    print(pagetype_analysis.head(10).to_string(index=False))
    
    print("\nOutput files have been saved to the 'output' directory:")
    print("- complete_dataset.csv: Full joined dataset with all URLs and their properties")
    print("- urls_to_remove_from_sitemap.csv: URLs currently in sitemaps that should be removed")
    print("- valid_sitemap_urls.csv: URLs correctly included in sitemaps")
    print("- missing_indexable_urls.csv: Indexable URLs that could be added to sitemaps")
    print("- pagetype_analysis.csv: Analysis of indexability by pagetype")
    print("- sitemap_analysis.csv: Analysis of issues by specific sitemap")

if __name__ == "__main__":
    process_urls_and_sitemaps(
        'combined_botify_export.csv',
        'all_extracted_urls.csv',
        './output'
    )