f = open("files.zip", "rb")
lines = f.readlines()
byte_list = []

# File represents a single file in a Zip file
class File:
    def __init__(self, name, size):
        self.name = name
        self.size = size


def find_end_of_name(start_count: int, data: list) -> int:
    count = start_count
    # the string 'UT' marks the end of a file name
    while data[count] != b'U' and data[count + 1] != b'T':
        count += 1
    return count
    
def find_end_of_data(start_count: int, data: list) -> int:
    count = start_count
    length = 0
    while data[count] != b'\n':
        count += 1
        length += 1
    return length

# open file and read in byte by byte
with open("files.zip", "rb") as f:
    while True:
        byte = f.read(1)
        if byte == b'0x20':
            continue

        if not byte:
            break
        byte_list.append(byte)

count = 0
for count in range(len(byte_list)):
    try: 
        # detect start of a new local file header
        if byte_list[count] == b'P' and byte_list[count + 1] == b'K':
            end_name_index = find_end_of_name(count + 30, byte_list)
            data = find_end_of_data(count + 63, byte_list)
            name = byte_list[count + 30:end_name_index]
            print(name, data)
            #print(byte_list[count+63:count+67])

        #print(count, byte_list[count].decode('utf-8'), byte_list[count])
    except Exception as e: 
        pass # ignore any errors
    count += 1

print(len(byte_list))
f.close()