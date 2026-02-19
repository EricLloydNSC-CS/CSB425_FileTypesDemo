# CSB425_FileTypesDemo

A demonstration project that converts CSV data to various columnar file formats (Avro, Parquet, and ORC) and compares their sizes and internal structures.

## Overview

This project demonstrates the conversion of CSV data into three popular big data file formats:
- **Avro**: A row-based format with rich schema support
- **Parquet**: A columnar format optimized for analytics
- **ORC**: Optimized Row Columnar format with efficient compression

## Features

- Convert CSV data to Avro, Parquet, and ORC formats
- Display file sizes and compression ratios
- Show internal structures and schemas
- Compare storage efficiency across formats

## Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/EricLloydNSC-CS/CSB425_FileTypesDemo.git
cd CSB425_FileTypesDemo
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the file converter demo:
```bash
python file_converter.py
```

The script will:
1. Read the sample CSV file (`sample_data.csv`)
2. Convert it to Avro, Parquet, and ORC formats
3. Display the schema and structure of each format
4. Show file sizes and compression ratios
5. Compare the storage efficiency

## Sample Output

The demo processes a sample employee dataset with the following fields:
- id (integer)
- name (string)
- age (integer)
- city (string)
- salary (float)
- hire_date (string)

## Files

- `file_converter.py` - Main conversion script
- `sample_data.csv` - Sample CSV data file
- `requirements.txt` - Python dependencies

## Dependencies

- pandas: Data manipulation and analysis
- pyarrow: Reading/writing Parquet and ORC files
- fastavro: Reading/writing Avro files

## Output Files

The script generates the following files (not committed to git):
- `sample_data.avro` - Avro format
- `sample_data.parquet` - Parquet format
- `sample_data.orc` - ORC format