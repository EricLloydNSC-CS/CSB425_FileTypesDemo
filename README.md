# CSB425_FileTypesDemo

A demonstration project that converts CSV data to various columnar file formats (Avro, Parquet, and ORC) and compares their sizes and internal structures, showcasing compression benefits at scale.

## Overview

This project demonstrates the conversion of CSV data into three popular big data file formats:
- **Avro**: A row-based format with rich schema support and binary encoding
- **Parquet**: A columnar format optimized for analytics with excellent compression
- **ORC**: Optimized Row Columnar format with efficient compression

The demo uses a large dataset (100,000 records) to showcase real-world compression benefits that become apparent at scale.

## Features

- Generate large CSV datasets with realistic employee data
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

### Generate Large CSV Dataset

First, generate a large CSV file with 100,000 employee records:
```bash
python generate_large_csv.py 100000
```

You can specify a different number of records as a command-line argument.

### Run the File Converter Demo

Convert the CSV to different formats and see the compression results:
```bash
python file_converter.py
```

The script will:
1. Read the sample CSV file (`sample_data.csv`)
2. Convert it to Avro, Parquet, and ORC formats
3. Display the schema and structure of each format
4. Show file sizes and compression ratios
5. Compare the storage efficiency

## Compression Results

With 100,000 employee records (~6 MB CSV), the compression results demonstrate significant storage savings:

```
CSV:      5.94 MB (100% - baseline)
Avro:     5.27 MB (88.7% - 11% space savings)
Parquet:  1.91 MB (32.1% - 68% space savings!)
ORC:      4.88 MB (82.2% - 18% space savings)
```

### Why Parquet Shows Best Compression?

- **Columnar storage**: Stores data by column rather than by row, allowing similar values to be grouped together
- **Efficient encoding**: Uses dictionary encoding, run-length encoding, and bit-packing
- **Compression algorithms**: Applies compression (Snappy) on columnar data which compresses much better than row data
- **Repeated values**: Departments, cities, and date patterns compress extremely well

### Why This Matters for Big Data?

At scale (millions or billions of records), these compression ratios translate to:
- **Reduced storage costs**: 68% less storage needed with Parquet
- **Faster query performance**: Less data to read from disk
- **Lower network transfer costs**: Smaller files mean less bandwidth usage
- **Better cache utilization**: More data fits in memory

## Sample Data

The demo processes employee data with the following fields:
- id (integer)
- name (string)
- age (integer)
- city (string)
- salary (float)
- hire_date (string)
- department (string)

## Files

- `generate_large_csv.py` - Script to generate large CSV datasets
- `file_converter.py` - Main conversion script
- `sample_data.csv` - Generated CSV data file (created by generate_large_csv.py)
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