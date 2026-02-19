#!/usr/bin/env python3
"""
CSV to Avro, Parquet, and ORC Converter
Demonstrates the differences in file sizes and structures between these formats.
"""

import os
import sys
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
import pyarrow.orc as orc
from fastavro import writer, reader, parse_schema
from pathlib import Path
import json


def read_csv_data(csv_file):
    """Read CSV file into a pandas DataFrame."""
    print(f"\n{'='*60}")
    print(f"Reading CSV file: {csv_file}")
    print(f"{'='*60}")
    
    df = pd.read_csv(csv_file)
    print(f"Rows: {len(df)}")
    print(f"Columns: {list(df.columns)}")
    print(f"\nFirst few rows:")
    print(df.head())
    
    return df


def convert_to_avro(df, output_file):
    """Convert DataFrame to Avro format."""
    print(f"\n{'='*60}")
    print("Converting to Avro format...")
    print(f"{'='*60}")
    
    # Define Avro schema
    avro_schema = {
        "type": "record",
        "name": "Employee",
        "fields": [
            {"name": "id", "type": "long"},
            {"name": "name", "type": "string"},
            {"name": "age", "type": "long"},
            {"name": "salary", "type": "double"},
            {"name": "department", "type": "string"},
            {"name": "join_date", "type": "string"}
        ]
    }
    
    # Convert DataFrame to list of dictionaries
    records = df.to_dict('records')
    
    # Write to Avro file
    parsed_schema = parse_schema(avro_schema)
    with open(output_file, 'wb') as out:
        writer(out, parsed_schema, records)
    
    print(f"✓ Avro file created: {output_file}")
    return avro_schema


def convert_to_parquet(df, output_file):
    """Convert DataFrame to Parquet format."""
    print(f"\n{'='*60}")
    print("Converting to Parquet format...")
    print(f"{'='*60}")
    
    # Convert to PyArrow Table
    table = pa.Table.from_pandas(df)
    
    # Write to Parquet file with compression
    pq.write_table(table, output_file, compression='snappy')
    
    print(f"✓ Parquet file created: {output_file}")
    return table.schema


def convert_to_orc(df, output_file):
    """Convert DataFrame to ORC format."""
    print(f"\n{'='*60}")
    print("Converting to ORC format...")
    print(f"{'='*60}")
    
    # Convert to PyArrow Table
    table = pa.Table.from_pandas(df)
    
    # Write to ORC file
    orc.write_table(table, output_file)
    
    print(f"✓ ORC file created: {output_file}")
    return table.schema


def compare_file_sizes(csv_file, avro_file, parquet_file, orc_file):
    """Compare file sizes of different formats."""
    print(f"\n{'='*60}")
    print("FILE SIZE COMPARISON")
    print(f"{'='*60}")
    
    csv_size = os.path.getsize(csv_file)
    avro_size = os.path.getsize(avro_file)
    parquet_size = os.path.getsize(parquet_file)
    orc_size = os.path.getsize(orc_file)
    
    print(f"\n{'Format':<15} {'Size (bytes)':<15} {'Size (KB)':<15} {'% of CSV':<15}")
    print("-" * 60)
    print(f"{'CSV':<15} {csv_size:<15} {csv_size/1024:<15.2f} {100.0:<15.1f}")
    print(f"{'Avro':<15} {avro_size:<15} {avro_size/1024:<15.2f} {(avro_size/csv_size)*100:<15.1f}")
    print(f"{'Parquet':<15} {parquet_size:<15} {parquet_size/1024:<15.2f} {(parquet_size/csv_size)*100:<15.1f}")
    print(f"{'ORC':<15} {orc_size:<15} {orc_size/1024:<15.2f} {(orc_size/csv_size)*100:<15.1f}")
    
    # Find the most efficient format
    sizes = {
        'Avro': avro_size,
        'Parquet': parquet_size,
        'ORC': orc_size
    }
    most_efficient = min(sizes, key=sizes.get)
    print(f"\n✓ Most space-efficient format: {most_efficient} ({sizes[most_efficient]} bytes)")


def show_avro_structure(avro_file):
    """Display Avro file structure."""
    print(f"\n{'='*60}")
    print("AVRO FILE STRUCTURE")
    print(f"{'='*60}")
    
    with open(avro_file, 'rb') as f:
        avro_reader = reader(f)
        schema = avro_reader.writer_schema
        
        print("\nSchema:")
        print(json.dumps(schema, indent=2))
        
        print("\nSample records (first 3):")
        records = list(avro_reader)
        for i, record in enumerate(records[:3], 1):
            print(f"\nRecord {i}:")
            for key, value in record.items():
                print(f"  {key}: {value}")


def show_parquet_structure(parquet_file):
    """Display Parquet file structure."""
    print(f"\n{'='*60}")
    print("PARQUET FILE STRUCTURE")
    print(f"{'='*60}")
    
    # Read Parquet file metadata
    parquet_file_obj = pq.ParquetFile(parquet_file)
    
    print("\nSchema:")
    print(parquet_file_obj.schema)
    
    print(f"\nNumber of row groups: {parquet_file_obj.num_row_groups}")
    print(f"Total rows: {parquet_file_obj.metadata.num_rows}")
    
    print("\nColumn statistics:")
    for i in range(parquet_file_obj.num_row_groups):
        row_group = parquet_file_obj.metadata.row_group(i)
        print(f"\nRow Group {i}:")
        for j in range(row_group.num_columns):
            col = row_group.column(j)
            print(f"  Column '{col.path_in_schema}': {col.total_compressed_size} bytes compressed, {col.total_uncompressed_size} bytes uncompressed")
    
    print("\nSample data (first 3 rows):")
    table = parquet_file_obj.read()
    df = table.to_pandas()
    print(df.head(3).to_string())


def show_orc_structure(orc_file):
    """Display ORC file structure."""
    print(f"\n{'='*60}")
    print("ORC FILE STRUCTURE")
    print(f"{'='*60}")
    
    # Read ORC file
    orc_file_obj = orc.ORCFile(orc_file)
    
    print("\nSchema:")
    print(orc_file_obj.schema)
    
    print(f"\nNumber of stripes: {orc_file_obj.nstripes}")
    print(f"Number of rows: {orc_file_obj.nrows}")
    
    print("\nStripe statistics:")
    for i in range(orc_file_obj.nstripes):
        print(f"  Stripe {i}: {orc_file_obj.read_stripe(i).num_rows} rows")
    
    print("\nSample data (first 3 rows):")
    table = orc_file_obj.read()
    df = table.to_pandas()
    print(df.head(3).to_string())


def main():
    """Main function to orchestrate the conversion and comparison."""
    # Use default file or command line argument
    if len(sys.argv) > 1:
        csv_file = sys.argv[1]
    else:
        csv_file = "sample_data.csv"
    
    # Check if CSV file exists
    if not os.path.exists(csv_file):
        print(f"Error: CSV file '{csv_file}' not found!")
        print(f"Usage: python {sys.argv[0]} [csv_file]")
        sys.exit(1)
    
    # Define output files
    base_name = Path(csv_file).stem
    avro_file = f"{base_name}.avro"
    parquet_file = f"{base_name}.parquet"
    orc_file = f"{base_name}.orc"
    
    # Read CSV data
    df = read_csv_data(csv_file)
    
    # Convert to different formats
    avro_schema = convert_to_avro(df, avro_file)
    parquet_schema = convert_to_parquet(df, parquet_file)
    orc_schema = convert_to_orc(df, orc_file)
    
    # Compare file sizes
    compare_file_sizes(csv_file, avro_file, parquet_file, orc_file)
    
    # Show structure of each format
    show_avro_structure(avro_file)
    show_parquet_structure(parquet_file)
    show_orc_structure(orc_file)
    
    print(f"\n{'='*60}")
    print("SUMMARY")
    print(f"{'='*60}")
    print("\nKey Differences:")
    print("• CSV: Plain text format, human-readable, no compression, largest size")
    print("• Avro: Row-based format, includes schema, supports compression, good for write-heavy workloads")
    print("• Parquet: Columnar format, excellent compression, optimized for read-heavy analytics")
    print("• ORC: Columnar format, highly optimized for Hadoop/Hive, includes column statistics")
    
    print("\nGenerated files:")
    print(f"  • {avro_file}")
    print(f"  • {parquet_file}")
    print(f"  • {orc_file}")
    print()


if __name__ == "__main__":
    main()
