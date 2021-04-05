f = open("files.zip", "rb")
lines = f.readlines()
byte_list = []

# File represents a single file in a Zip file
class File:
    def __init__(self, name, size):
        self.name = name
        self.size = size
    

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
            name = byte_list[count + 30:count + 35]
            print(name)
    except Exception as e: 
        pass # ignore any errors
    count += 1

print(len(byte_list))
f.close()