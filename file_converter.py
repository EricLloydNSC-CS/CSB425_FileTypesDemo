#!/usr/bin/env python3
"""
File Types Demo: CSV to Avro, Parquet, and ORC Converter

This script demonstrates conversion of CSV data to different file formats
(Avro, Parquet, and ORC) and displays their sizes and internal structures.
"""

import os
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
import pyarrow.orc as orc
from fastavro import writer, reader, parse_schema
from datetime import datetime


def get_file_size(filepath):
    """Get file size in bytes and return human-readable format."""
    size_bytes = os.path.getsize(filepath)
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} TB"


def read_csv(csv_path):
    """Read CSV file into a pandas DataFrame."""
    print(f"\n{'='*60}")
    print(f"Reading CSV file: {csv_path}")
    print(f"{'='*60}")
    
    df = pd.read_csv(csv_path)
    print(f"Records loaded: {len(df)}")
    print(f"\nData preview:")
    print(df.head())
    print(f"\nData types:")
    print(df.dtypes)
    
    return df


def convert_to_avro(df, output_path):
    """Convert DataFrame to Avro format."""
    print(f"\n{'='*60}")
    print("Converting to AVRO format")
    print(f"{'='*60}")
    
    # Define Avro schema
    schema = {
        'name': 'Employee',
        'type': 'record',
        'fields': [
            {'name': 'id', 'type': 'long'},
            {'name': 'name', 'type': 'string'},
            {'name': 'age', 'type': 'long'},
            {'name': 'city', 'type': 'string'},
            {'name': 'salary', 'type': 'double'},
            {'name': 'hire_date', 'type': 'string'}
        ]
    }
    
    parsed_schema = parse_schema(schema)
    
    # Convert DataFrame to list of dicts
    records = df.to_dict('records')
    
    # Write to Avro file
    with open(output_path, 'wb') as out:
        writer(out, parsed_schema, records)
    
    print(f"✓ Avro file created: {output_path}")
    print(f"  File size: {get_file_size(output_path)}")
    
    # Display schema
    print(f"\n  Schema:")
    for field in schema['fields']:
        print(f"    - {field['name']}: {field['type']}")
    
    # Read back and show sample
    with open(output_path, 'rb') as avro_file:
        avro_reader = reader(avro_file)
        print(f"\n  Sample records (first 3):")
        for i, record in enumerate(avro_reader):
            if i >= 3:
                break
            print(f"    {record}")


def convert_to_parquet(df, output_path):
    """Convert DataFrame to Parquet format."""
    print(f"\n{'='*60}")
    print("Converting to PARQUET format")
    print(f"{'='*60}")
    
    # Convert to PyArrow Table
    table = pa.Table.from_pandas(df)
    
    # Write to Parquet file with compression
    pq.write_table(table, output_path, compression='snappy')
    
    print(f"✓ Parquet file created: {output_path}")
    print(f"  File size: {get_file_size(output_path)}")
    
    # Read back and display metadata
    parquet_file = pq.ParquetFile(output_path)
    
    print(f"\n  Schema:")
    print(f"    {parquet_file.schema}")
    
    print(f"\n  Metadata:")
    print(f"    - Rows: {parquet_file.metadata.num_rows}")
    print(f"    - Columns: {parquet_file.metadata.num_columns}")
    print(f"    - Row groups: {parquet_file.metadata.num_row_groups}")
    print(f"    - Compression: snappy")
    
    # Show sample data
    print(f"\n  Sample records (first 3):")
    table = parquet_file.read()
    sample_df = table.to_pandas().head(3)
    for idx, row in sample_df.iterrows():
        print(f"    {row.to_dict()}")


def convert_to_orc(df, output_path):
    """Convert DataFrame to ORC format."""
    print(f"\n{'='*60}")
    print("Converting to ORC format")
    print(f"{'='*60}")
    
    # Convert to PyArrow Table
    table = pa.Table.from_pandas(df)
    
    # Write to ORC file
    orc.write_table(table, output_path)
    
    print(f"✓ ORC file created: {output_path}")
    print(f"  File size: {get_file_size(output_path)}")
    
    # Read back and display metadata
    orc_file = orc.ORCFile(output_path)
    
    print(f"\n  Schema:")
    print(f"    {orc_file.schema}")
    
    print(f"\n  Metadata:")
    print(f"    - Rows: {orc_file.nrows}")
    print(f"    - Stripes: {orc_file.nstripes}")
    
    # Show sample data
    print(f"\n  Sample records (first 3):")
    table = orc_file.read()
    sample_df = table.to_pandas().head(3)
    for idx, row in sample_df.iterrows():
        print(f"    {row.to_dict()}")


def display_size_comparison(csv_path, avro_path, parquet_path, orc_path):
    """Display size comparison of all formats."""
    print(f"\n{'='*60}")
    print("FILE SIZE COMPARISON")
    print(f"{'='*60}")
    
    csv_size = os.path.getsize(csv_path)
    avro_size = os.path.getsize(avro_path)
    parquet_size = os.path.getsize(parquet_path)
    orc_size = os.path.getsize(orc_path)
    
    print(f"CSV:     {get_file_size(csv_path):>12} ({csv_size} bytes)")
    print(f"Avro:    {get_file_size(avro_path):>12} ({avro_size} bytes) - {(avro_size/csv_size)*100:.1f}% of CSV")
    print(f"Parquet: {get_file_size(parquet_path):>12} ({parquet_size} bytes) - {(parquet_size/csv_size)*100:.1f}% of CSV")
    print(f"ORC:     {get_file_size(orc_path):>12} ({orc_size} bytes) - {(orc_size/csv_size)*100:.1f}% of CSV")
    
    # Determine smallest format
    sizes = {
        'CSV': csv_size,
        'Avro': avro_size,
        'Parquet': parquet_size,
        'ORC': orc_size
    }
    smallest = min(sizes, key=sizes.get)
    print(f"\n✓ Smallest format: {smallest}")


def main():
    """Main function to run the file conversion demo."""
    print("\n" + "="*60)
    print("FILE TYPES DEMO: CSV to Avro, Parquet, and ORC")
    print("="*60)
    
    # Define file paths
    csv_path = "sample_data.csv"
    avro_path = "sample_data.avro"
    parquet_path = "sample_data.parquet"
    orc_path = "sample_data.orc"
    
    # Check if CSV file exists
    if not os.path.exists(csv_path):
        print(f"Error: {csv_path} not found!")
        return
    
    # Read CSV
    df = read_csv(csv_path)
    
    # Convert to different formats
    convert_to_avro(df, avro_path)
    convert_to_parquet(df, parquet_path)
    convert_to_orc(df, orc_path)
    
    # Display size comparison
    display_size_comparison(csv_path, avro_path, parquet_path, orc_path)
    
    print(f"\n{'='*60}")
    print("Conversion complete! All files created successfully.")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()
