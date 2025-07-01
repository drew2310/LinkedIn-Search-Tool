import pandas as pd

# Create data
data = {
    'First Name': ['Oren', 'Ariel', 'Soham', 'Andrew', 'Dasrsh', 'Dylan','Byron', 'Arian', 'Karma', 'Fred'],
    'Last Name': ['Rabinovich', 'Gitman', 'Desai', 'Jerome', 'Patel', 'Shah', 'Gomez', 'Pedram', 'Tenzin', 'Ngo'],
    'University': ['Rutgers University','Rutgers University','Rutgers University', 'Rutgers University', 'Rutgers University', 'Rutgers University', 'Rutgers University', 'Rutgers University', 'Rutgers University', 'University of Toronto'],
    'School City': ['','Newark', 'Newark', 'Newark', 'Newark', 'Newark', 'Newark', 'Newark', 'Newark', 'Toronto'],
    'School State': ['','New Jersey', 'New Jersey', 'New Jersey', 'New Jersey', 'New Jersey', 'New Jersey', 'New Jersey', 'New Jersey', 'Ontario'],
    'School Country': ['','United States', 'United States', 'United States', 'United States', 'United States', 'United States', 'United States', 'United States', 'Canada'],
    'Residence City': ['','', '', '', '', '', '', '', '', ''],
    'Residence State': ['','New Jersey', 'New Jersey', 'New Jersey', 'New Jersey', 'New Jersey', 'New Jersey', 'New Jersey', 'New Jersey', ''],    
    'Degree Program': ['','Computer Science', 'Computer Science', 'Computer Science', 'Computer Science', 'Computer Science', 'Computer Science', 'Computer Science', 'Computer Science', ''],
    'Graduation Year': [2022, 2025, 2025, 2025, 2025, 2025, 2025, 2025, 2025, 1998],
    }

# Create DataFrame and save to CSV
df = pd.DataFrame(data)
df.to_csv('names_with_university.csv', index=False)
print("CSV with university information created successfully.")