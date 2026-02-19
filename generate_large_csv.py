#!/usr/bin/env python3
"""
Generate a large CSV file with realistic employee data for demonstrating
compression benefits of Avro, Parquet, and ORC formats.
"""

import csv
import random
from datetime import datetime, timedelta

# Sample data for realistic generation
FIRST_NAMES = [
    'James', 'Mary', 'John', 'Patricia', 'Robert', 'Jennifer', 'Michael', 'Linda',
    'William', 'Barbara', 'David', 'Elizabeth', 'Richard', 'Susan', 'Joseph', 'Jessica',
    'Thomas', 'Sarah', 'Charles', 'Karen', 'Christopher', 'Nancy', 'Daniel', 'Lisa',
    'Matthew', 'Betty', 'Anthony', 'Margaret', 'Mark', 'Sandra', 'Donald', 'Ashley',
    'Steven', 'Kimberly', 'Paul', 'Emily', 'Andrew', 'Donna', 'Joshua', 'Michelle',
    'Kenneth', 'Dorothy', 'Kevin', 'Carol', 'Brian', 'Amanda', 'George', 'Melissa',
    'Edward', 'Deborah', 'Ronald', 'Stephanie', 'Timothy', 'Rebecca', 'Jason', 'Sharon',
    'Jeffrey', 'Laura', 'Ryan', 'Cynthia', 'Jacob', 'Kathleen', 'Gary', 'Amy',
    'Nicholas', 'Shirley', 'Eric', 'Angela', 'Jonathan', 'Helen', 'Stephen', 'Anna',
    'Larry', 'Brenda', 'Justin', 'Pamela', 'Scott', 'Nicole', 'Brandon', 'Emma',
    'Benjamin', 'Samantha', 'Samuel', 'Katherine', 'Frank', 'Christine', 'Gregory', 'Debra',
    'Raymond', 'Rachel', 'Alexander', 'Catherine', 'Patrick', 'Carolyn', 'Jack', 'Janet',
    'Dennis', 'Ruth', 'Jerry', 'Maria', 'Tyler', 'Heather', 'Aaron', 'Diane'
]

LAST_NAMES = [
    'Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis',
    'Rodriguez', 'Martinez', 'Hernandez', 'Lopez', 'Gonzalez', 'Wilson', 'Anderson', 'Thomas',
    'Taylor', 'Moore', 'Jackson', 'Martin', 'Lee', 'Perez', 'Thompson', 'White',
    'Harris', 'Sanchez', 'Clark', 'Ramirez', 'Lewis', 'Robinson', 'Walker', 'Young',
    'Allen', 'King', 'Wright', 'Scott', 'Torres', 'Nguyen', 'Hill', 'Flores',
    'Green', 'Adams', 'Nelson', 'Baker', 'Hall', 'Rivera', 'Campbell', 'Mitchell',
    'Carter', 'Roberts', 'Gomez', 'Phillips', 'Evans', 'Turner', 'Diaz', 'Parker',
    'Cruz', 'Edwards', 'Collins', 'Reyes', 'Stewart', 'Morris', 'Morales', 'Murphy',
    'Cook', 'Rogers', 'Gutierrez', 'Ortiz', 'Morgan', 'Cooper', 'Peterson', 'Bailey',
    'Reed', 'Kelly', 'Howard', 'Ramos', 'Kim', 'Cox', 'Ward', 'Richardson',
    'Watson', 'Brooks', 'Chavez', 'Wood', 'James', 'Bennett', 'Gray', 'Mendoza',
    'Ruiz', 'Hughes', 'Price', 'Alvarez', 'Castillo', 'Sanders', 'Patel', 'Myers',
    'Long', 'Ross', 'Foster', 'Jimenez', 'Powell', 'Jenkins', 'Perry', 'Russell'
]

CITIES = [
    'New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix', 'Philadelphia',
    'San Antonio', 'San Diego', 'Dallas', 'San Jose', 'Austin', 'Jacksonville',
    'Fort Worth', 'Columbus', 'Charlotte', 'San Francisco', 'Indianapolis', 'Seattle',
    'Denver', 'Washington', 'Boston', 'El Paso', 'Nashville', 'Detroit', 'Oklahoma City',
    'Portland', 'Las Vegas', 'Memphis', 'Louisville', 'Baltimore', 'Milwaukee', 'Albuquerque',
    'Tucson', 'Fresno', 'Sacramento', 'Kansas City', 'Long Beach', 'Mesa', 'Atlanta',
    'Colorado Springs', 'Virginia Beach', 'Raleigh', 'Omaha', 'Miami', 'Oakland',
    'Minneapolis', 'Tulsa', 'Wichita', 'New Orleans', 'Arlington'
]

# Salary ranges by department
DEPARTMENTS = {
    'Engineering': (70000, 150000),
    'Sales': (50000, 120000),
    'Marketing': (55000, 110000),
    'HR': (50000, 95000),
    'Finance': (60000, 130000),
    'Operations': (45000, 90000),
    'Customer Service': (35000, 70000),
    'IT': (65000, 140000),
    'Legal': (80000, 180000),
    'Research': (60000, 120000)
}


def random_date(start_year=2015, end_year=2023):
    """Generate a random date between start_year and end_year."""
    start_date = datetime(start_year, 1, 1)
    end_date = datetime(end_year, 12, 31)
    time_between = end_date - start_date
    random_days = random.randrange(time_between.days)
    return (start_date + timedelta(days=random_days)).strftime('%Y-%m-%d')


def generate_employee_record(emp_id):
    """Generate a single employee record."""
    first_name = random.choice(FIRST_NAMES)
    last_name = random.choice(LAST_NAMES)
    name = f"{first_name} {last_name}"
    age = random.randint(22, 65)
    city = random.choice(CITIES)
    department = random.choice(list(DEPARTMENTS.keys()))
    salary_min, salary_max = DEPARTMENTS[department]
    salary = round(random.uniform(salary_min, salary_max), 2)
    hire_date = random_date()
    
    return [emp_id, name, age, city, salary, hire_date, department]


def generate_large_csv(filename='sample_data.csv', num_records=100000):
    """Generate a large CSV file with employee data."""
    print(f"Generating {num_records:,} employee records...")
    
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        # Write header
        writer.writerow(['id', 'name', 'age', 'city', 'salary', 'hire_date', 'department'])
        
        # Write records
        for i in range(1, num_records + 1):
            writer.writerow(generate_employee_record(i))
            
            if i % 10000 == 0:
                print(f"  Generated {i:,} records...")
    
    import os
    file_size = os.path.getsize(filename)
    print(f"\n✓ Generated {filename}")
    print(f"  Records: {num_records:,}")
    print(f"  File size: {file_size:,} bytes ({file_size / (1024*1024):.2f} MB)")


if __name__ == "__main__":
    import sys
    
    # Allow custom number of records via command line
    num_records = 100000
    if len(sys.argv) > 1:
        try:
            num_records = int(sys.argv[1])
        except ValueError:
            print(f"Invalid number: {sys.argv[1]}, using default of 100,000")
    
    generate_large_csv(num_records=num_records)
