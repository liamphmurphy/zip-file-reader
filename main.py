import argparse

# File represents a single file in a Zip file
class File:
    def __init__(self, name, size):
        self.name = name
        self.size = size


# counts at what point the end of the name occurs in the byte array
def find_end_of_name(start_count: int, data: list) -> int:
    count = start_count
    # the string 'UT' marks the end of a file name
    while data[count] != b'U' and data[count + 1] != b'T':
        count += 1
    return count
    
# counts at what point the end of the data occurs in the byte array
def find_end_of_data(start_count: int, data: list) -> int:
    count = start_count
    length = 0
    while data[count] != b'P' and data[count + 1] != b'K':
        count += 1
        length += 1
    return length

# offsets assume that the program has found the beginning 'PK' string before a file
offsets = {
    "name": 30,
    "data": 63
}

zip_file = open("files.zip", "rb")
lines = zip_file.readlines()
byte_list = []

# parse passed in arguments
parser = argparse.ArgumentParser(description="Prints the name and size of each file in a zip archive.")
parser.add_argument('-p', action="store_true", help="prints all data from the byte array, instead of just the found files.")
args = parser.parse_args()

# open file and read in byte by byte
with open("files.zip", "rb") as f:
    while True:
        byte = f.read(1)

        if not byte:
            break
        byte_list.append(byte)

# begin parsing
count = 0
found_files = list() # list of File objects
for count in range(len(byte_list)):
    try: 
        # detect start of a new local file header
        if byte_list[count] == b'P' and byte_list[count + 1] == b'K':
            end_name_index = find_end_of_name(count + offsets["name"], byte_list)
            name = byte_list[count + offsets["name"]:end_name_index]
            if name[0] == b'\x18':
                continue
            data = find_end_of_data(count + offsets["data"], byte_list)
            found_files.append(File(b''.join(name).decode('utf-8'), data))
            #print(name, data)
            #print(byte_list[count+63:count+67])

        #print(count, byte_list[count].decode('utf-8'), byte_list[count])
    except Exception as e:
        pass # ignore any errors
    count += 1

# if specified, print the entire byte array from the zip archive
if args.p:
    for i in range(len(byte_list)):
        print(i, byte_list[i])

for f in found_files:
    print(f.name, f.size)

print("size of zip archive:", len(byte_list))
zip_file.close()