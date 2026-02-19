# CSB425 File Types Demo

A demonstration script that converts CSV data to different columnar and row-based file formats (Avro, Parquet, and ORC) and compares their characteristics.

## Overview

This project demonstrates the differences between various data storage formats commonly used in big data and analytics:

- **CSV**: Plain text, human-readable, no compression
- **Avro**: Row-based binary format with embedded schema
- **Parquet**: Columnar format optimized for analytics
- **ORC**: Columnar format optimized for Hadoop ecosystem

## Features

- 📊 **Convert CSV to multiple formats**: Avro, Parquet, and ORC
- 📏 **File size comparison**: See how different formats affect storage
- 🔍 **Structure inspection**: View internal structure and schema of each format
- 📈 **Sample data included**: Ready-to-run with example employee data

## Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- pandas (data manipulation)
- pyarrow (Parquet and ORC support)
- fastavro (Avro support)

## Usage

### Basic Usage

Run with the included sample data:

```bash
python convert_csv.py
```

### Using Your Own CSV File

```bash
python convert_csv.py your_data.csv
```

## Output

The script will:

1. **Read the CSV file** and display basic statistics
2. **Convert to Avro, Parquet, and ORC formats**
3. **Compare file sizes** showing:
   - Absolute sizes in bytes and KB
   - Relative sizes as percentage of original CSV
   - Most space-efficient format
4. **Display internal structures** including:
   - Schema definitions
   - Column statistics
   - Compression details
   - Sample records

### Example Output

```
============================================================
FILE SIZE COMPARISON
============================================================

Format          Size (bytes)    Size (KB)       % of CSV       
------------------------------------------------------------
CSV             515             0.50            100.0          
Avro            776             0.76            150.7          
Parquet         4744            4.63            921.2          
ORC             1345            1.31            261.2          

✓ Most space-efficient format: Avro (776 bytes)
```

## Generated Files

The script creates three output files:

- `<filename>.avro` - Avro format file
- `<filename>.parquet` - Parquet format file
- `<filename>.orc` - ORC format file

## Sample Data

The included `sample_data.csv` contains employee records with:
- ID (integer)
- Name (string)
- Age (integer)
- Salary (decimal)
- Department (string)
- Join Date (date string)

## Key Differences Between Formats

| Feature | CSV | Avro | Parquet | ORC |
|---------|-----|------|---------|-----|
| **Type** | Text | Binary | Binary | Binary |
| **Layout** | Row-based | Row-based | Columnar | Columnar |
| **Schema** | None | Embedded | Embedded | Embedded |
| **Compression** | None | Optional | Yes | Yes |
| **Best For** | Small data, interchange | Write-heavy, streaming | Analytics, queries | Hadoop, Hive |
| **Human Readable** | Yes | No | No | No |

## Use Cases

- **CSV**: Data interchange, small datasets, human inspection
- **Avro**: Event streaming, Kafka, write-heavy workloads
- **Parquet**: Data lakes, analytical queries, Spark/Presto
- **ORC**: Hive tables, Hadoop ecosystem, columnar analytics

## Technical Details

### Avro
- Row-oriented format storing data with schema
- Supports schema evolution
- Fast serialization/deserialization
- Good for sequential processing

### Parquet
- Columnar storage with nested data support
- Excellent compression ratios
- Efficient predicate pushdown
- Ideal for SELECT queries on specific columns

### ORC
- Highly optimized columnar format
- Built-in column statistics and indexes
- Lightweight indexes for fast lookups
- Optimized for Hive and Hadoop

## License

This is a demonstration project for educational purposes.