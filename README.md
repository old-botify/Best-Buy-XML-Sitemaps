# Sitemap URL Analysis Tool

## Files in Google Drive
These are exports from the code. [The Data Can Be Found Here](https://drive.google.com/drive/folders/1ER5NbTm7ANLBKqgKWqVJJ-bXMNf-fN-0?usp=sharing)

## ⚠️ Known Issues
- **complete_dataset.csv**: Currently only contains non-indexable URLs. Needs to be updated to include all URLs
- **urls_to_remove_from_sitemap.csv**: Currently showing incorrect data (showing indexable URLs instead of non-indexable). Needs to be fixed
- **valid_sitemap_urls.csv**: Output appears to be broken/incorrect
- **missing_indexable_urls.csv**: Output appears to be broken/incorrect

## Overview
This tool combines and analyzes URLs from Botify exports and XML sitemaps to identify indexability issues and provide QA insights. It helps identify URLs that should be removed from sitemaps and provides analysis by pagetype.

## Prerequisites
- Python 3.8+
- pandas
- tqdm

## Installation
1. Clone this repository
2. Install required packages:
```bash
pip install -r requirements.txt
```

## Project Structure
```
sitemap-analysis/
├── README.md
├── .gitignore
├── requirements.txt
├── botify-combine.py
├── lookup.py
├── botify_export/         # Directory for individual Botify export CSVs
└── output/               # Generated analysis files
    ├── complete_dataset.csv
    ├── urls_to_remove_from_sitemap.csv
    ├── valid_sitemap_urls.csv
    ├── missing_indexable_urls.csv
    ├── pagetype_analysis.csv
    └── sitemap_analysis.csv
```

## Scripts

### 1. botify-combine.py
Combines multiple Botify export CSV files into a single consolidated file.

#### Features:
- Handles 'sep=,' headers automatically
- Removes duplicate entries
- Adds source file tracking
- Provides summary statistics after combining

#### Usage:
1. Place all Botify export CSV files in the `botify_export/` directory
2. Run:
```bash
python botify-combine.py
```
This will generate `combined_botify_export.csv` in the root directory.

### 2. lookup.py
Analyzes the combined Botify data with sitemap data to identify indexability issues.

#### Usage:
After running botify-combine.py, run:
```bash
python lookup.py
```

## Input Files Required

### For botify-combine.py:
- Multiple Botify export CSV files in the `botify_export/` directory

### For lookup.py:
1. **combined_botify_export.csv**: Combined Botify export (generated from botify-combine.py) containing:
   - Full URL
   - pagetype
   - Non-Indexable Main Reason
   - Other Botify metrics
   - source_file (added during combination)

2. **all_extracted_urls.csv**: XML sitemap data containing:
   - URL
   - Source Sitemap

## Output Files
All analysis outputs are saved to the `output/` directory:

1. **complete_dataset.csv**
   - Combined dataset with Botify data and sitemap information
   - ⚠️ Currently only contains non-indexable URLs

2. **urls_to_remove_from_sitemap.csv**
   - URLs that should be removed from sitemaps (non-indexable)
   - ⚠️ Currently showing incorrect data

3. **valid_sitemap_urls.csv**
   - URLs correctly included in sitemaps
   - ⚠️ Currently broken/incorrect

4. **missing_indexable_urls.csv**
   - Indexable URLs not currently in sitemaps
   - ⚠️ Currently broken/incorrect

5. **pagetype_analysis.csv**
   - Analysis of indexability by pagetype

6. **sitemap_analysis.csv**
   - Analysis of issues by specific sitemap

## Workflow
1. Place all Botify export CSVs in `botify_export/` directory
2. Run `python botify-combine.py` to generate combined export
3. Ensure `all_extracted_urls.csv` is in the root directory
4. Run `python lookup.py` to generate analysis
5. Review results in the `output/` directory

## Contributing
1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License
MIT License - see LICENSE file for details