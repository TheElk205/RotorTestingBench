crc_mask = 0x35
crc_size = 6

def mask(nbit):
    ret = 1
    for i in range(0, nbit - 1):
        ret <<= 1
        ret |= 1
    return ret


def transmit(data, data_length):
    process_data = data << (crc_size - 1)
    position = 0
    check = 1 << (data_length + crc_size - 2)
    while position < crc_size:
        i = check & process_data
        if i == 0:
            check >>= 1
            position += 1
        else:
            process_data ^= (crc_mask << (data_length - 1 - position))
            check >>= 1
            position += 1
    m = mask(crc_size - 1)
    lastndigits = m & process_data
    return (data << (crc_size - 1)) | lastndigits


def check_transmitted(transmitted, length):
    process_data = transmitted << (crc_size - 1)
    position = 0
    check = 1 << (length + crc_size - 2)
    while position < crc_size:
        i = check & process_data
        if i == 0:
            check >>= 1
            position += 1
        else:
            process_data ^= (crc_mask << (length - 1 - position))
            check >>= 1
            position += 1
    if process_data == 0:
        return True
    else:
        return False

data = 0x1B

recieved = transmit(data, 5)
print(recieved)
print(check_transmitted(recieved, 10))
