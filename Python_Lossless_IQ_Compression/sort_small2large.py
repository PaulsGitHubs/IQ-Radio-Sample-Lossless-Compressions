import os

# Get all files in current directory
files = [f for f in os.listdir('.') if os.path.isfile(f)]

# Get sizes and sort files by size
sorted_files = sorted(files, key=os.path.getsize)

for file in sorted_files:
    size_bytes = os.path.getsize(file)
    size_mb = size_bytes / (1024 * 1024)  # Convert to MB
    print(f'{file}: {size_mb:.2f} MB')
