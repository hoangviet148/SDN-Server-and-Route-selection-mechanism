input = "14:c4:e1:2a:91:1c:da:2a:ab:b8:0f:27:93:b6:15:0d:c5:b5:bf:f9:7d:e2:18:cb:ce:ab:44:d0"

def string_hex_to_int(hex_string):
    for i in range(0, len(hex_string), 3):
        print(i, hex_string[i:i+2], int(hex_string[i:i+2], 16))
        
    # return [int(hex_string[i:i+2], 16) for i in range(0, len(hex_string), 2)]

string_hex_to_int(input)