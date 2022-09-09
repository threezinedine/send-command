def convert_string_to_hex(string):
    return bytearray.fromhex(string)

def convert_hex_to_string(hexStr):
    result = hexStr.hex()
    if len(result) % 2 != 0:
        result = "0" + result

    index = 0
    byteIndex = 0
    length = len(result)/2

    formattedStr = ""

    while byteIndex < length:
        formattedStr += result[index: index + 2] 

        if byteIndex < length - 1:
            formattedStr += " "

        index += 2
        byteIndex += 1
    return formattedStr
