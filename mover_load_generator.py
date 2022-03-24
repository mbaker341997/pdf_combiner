import os

# Generates 10,000 files to load test the system on
PREFIX_1 = '1234567'
PREFIX_2 = '7654321'


def create_file(filename):
    with open(filename, 'w') as f:
        f.write("fooooooooooooooooooooooooo")

directory_path = input("Enter directory path: ")
full_path = f'{directory_path}/mover_load'
if not os.path.exists(full_path):
    os.makedirs(full_path)
for x in range(5000):
    create_file(f'{full_path}/{PREFIX_1}.{x}.txt')
    create_file(f'{full_path}/{PREFIX_2}.{x}.txt')

