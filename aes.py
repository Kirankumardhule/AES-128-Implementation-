#AES-128 Implementation with Round-wise Output
#Author: [Kirankumar Dhule]
#References:
#- NIST FIPS 197 (AES Standard): https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.197.pdf
#- Rijndael S-box/MixColumns theory (Daemen & Rijmen)

# S-box and Inverse S-box
s_box = [
    0x63, 0x7C, 0x77, 0x7B, 0xF2, 0x6B, 0x6F, 0xC5, 0x30, 0x01, 0x67, 0x2B, 0xFE, 0xD7, 0xAB, 0x76,
    0xCA, 0x82, 0xC9, 0x7D, 0xFA, 0x59, 0x47, 0xF0, 0xAD, 0xD4, 0xA2, 0xAF, 0x9C, 0xA4, 0x72, 0xC0,
    0xB7, 0xFD, 0x93, 0x26, 0x36, 0x3F, 0xF7, 0xCC, 0x34, 0xA5, 0xE5, 0xF1, 0x71, 0xD8, 0x31, 0x15,
    0x04, 0xC7, 0x23, 0xC3, 0x18, 0x96, 0x05, 0x9A, 0x07, 0x12, 0x80, 0xE2, 0xEB, 0x27, 0xB2, 0x75,
    0x09, 0x83, 0x2C, 0x1A, 0x1B, 0x6E, 0x5A, 0xA0, 0x52, 0x3B, 0xD6, 0xB3, 0x29, 0xE3, 0x2F, 0x84,
    0x53, 0xD1, 0x00, 0xED, 0x20, 0xFC, 0xB1, 0x5B, 0x6A, 0xCB, 0xBE, 0x39, 0x4A, 0x4C, 0x58, 0xCF,
    0xD0, 0xEF, 0xAA, 0xFB, 0x43, 0x4D, 0x33, 0x85, 0x45, 0xF9, 0x02, 0x7F, 0x50, 0x3C, 0x9F, 0xA8,
    0x51, 0xA3, 0x40, 0x8F, 0x92, 0x9D, 0x38, 0xF5, 0xBC, 0xB6, 0xDA, 0x21, 0x10, 0xFF, 0xF3, 0xD2,
    0xCD, 0x0C, 0x13, 0xEC, 0x5F, 0x97, 0x44, 0x17, 0xC4, 0xA7, 0x7E, 0x3D, 0x64, 0x5D, 0x19, 0x73,
    0x60, 0x81, 0x4F, 0xDC, 0x22, 0x2A, 0x90, 0x88, 0x46, 0xEE, 0xB8, 0x14, 0xDE, 0x5E, 0x0B, 0xDB,
    0xE0, 0x32, 0x3A, 0x0A, 0x49, 0x06, 0x24, 0x5C, 0xC2, 0xD3, 0xAC, 0x62, 0x91, 0x95, 0xE4, 0x79,
    0xE7, 0xC8, 0x37, 0x6D, 0x8D, 0xD5, 0x4E, 0xA9, 0x6C, 0x56, 0xF4, 0xEA, 0x65, 0x7A, 0xAE, 0x08,
    0xBA, 0x78, 0x25, 0x2E, 0x1C, 0xA6, 0xB4, 0xC6, 0xE8, 0xDD, 0x74, 0x1F, 0x4B, 0xBD, 0x8B, 0x8A,
    0x70, 0x3E, 0xB5, 0x66, 0x48, 0x03, 0xF6, 0x0E, 0x61, 0x35, 0x57, 0xB9, 0x86, 0xC1, 0x1D, 0x9E,
    0xE1, 0xF8, 0x98, 0x11, 0x69, 0xD9, 0x8E, 0x94, 0x9B, 0x1E, 0x87, 0xE9, 0xCE, 0x55, 0x28, 0xDF,
    0x8C, 0xA1, 0x89, 0x0D, 0xBF, 0xE6, 0x42, 0x68, 0x41, 0x99, 0x2D, 0x0F, 0xB0, 0x54, 0xBB, 0x16
]

inv_s_box = [
    0x52, 0x09, 0x6A, 0xD5, 0x30, 0x36, 0xA5, 0x38, 0xBF, 0x40, 0xA3, 0x9E, 0x81, 0xF3, 0xD7, 0xFB,
    0x7C, 0xE3, 0x39, 0x82, 0x9B, 0x2F, 0xFF, 0x87, 0x34, 0x8E, 0x43, 0x44, 0xC4, 0xDE, 0xE9, 0xCB,
    0x54, 0x7B, 0x94, 0x32, 0xA6, 0xC2, 0x23, 0x3D, 0xEE, 0x4C, 0x95, 0x0B, 0x42, 0xFA, 0xC3, 0x4E,
    0x08, 0x2E, 0xA1, 0x66, 0x28, 0xD9, 0x24, 0xB2, 0x76, 0x5B, 0xA2, 0x49, 0x6D, 0x8B, 0xD1, 0x25,
    0x72, 0xF8, 0xF6, 0x64, 0x86, 0x68, 0x98, 0x16, 0xD4, 0xA4, 0x5C, 0xCC, 0x5D, 0x65, 0xB6, 0x92,
    0x6C, 0x70, 0x48, 0x50, 0xFD, 0xED, 0xB9, 0xDA, 0x5E, 0x15, 0x46, 0x57, 0xA7, 0x8D, 0x9D, 0x84,
    0x90, 0xD8, 0xAB, 0x00, 0x8C, 0xBC, 0xD3, 0x0A, 0xF7, 0xE4, 0x58, 0x05, 0xB8, 0xB3, 0x45, 0x06,
    0xD0, 0x2C, 0x1E, 0x8F, 0xCA, 0x3F, 0x0F, 0x02, 0xC1, 0xAF, 0xBD, 0x03, 0x01, 0x13, 0x8A, 0x6B,
    0x3A, 0x91, 0x11, 0x41, 0x4F, 0x67, 0xDC, 0xEA, 0x97, 0xF2, 0xCF, 0xCE, 0xF0, 0xB4, 0xE6, 0x73,
    0x96, 0xAC, 0x74, 0x22, 0xE7, 0xAD, 0x35, 0x85, 0xE2, 0xF9, 0x37, 0xE8, 0x1C, 0x75, 0xDF, 0x6E,
    0x47, 0xF1, 0x1A, 0x71, 0x1D, 0x29, 0xC5, 0x89, 0x6F, 0xB7, 0x62, 0x0E, 0xAA, 0x18, 0xBE, 0x1B,
    0xFC, 0x56, 0x3E, 0x4B, 0xC6, 0xD2, 0x79, 0x20, 0x9A, 0xDB, 0xC0, 0xFE, 0x78, 0xCD, 0x5A, 0xF4,
    0x1F, 0xDD, 0xA8, 0x33, 0x88, 0x07, 0xC7, 0x31, 0xB1, 0x12, 0x10, 0x59, 0x27, 0x80, 0xEC, 0x5F,
    0x60, 0x51, 0x7F, 0xA9, 0x19, 0xB5, 0x4A, 0x0D, 0x2D, 0xE5, 0x7A, 0x9F, 0x93, 0xC9, 0x9C, 0xEF,
    0xA0, 0xE0, 0x3B, 0x4D, 0xAE, 0x2A, 0xF5, 0xB0, 0xC8, 0xEB, 0xBB, 0x3C, 0x83, 0x53, 0x99, 0x61,
    0x17, 0x2B, 0x04, 0x7E, 0xBA, 0x77, 0xD6, 0x26, 0xE1, 0x69, 0x14, 0x63, 0x55, 0x21, 0x0C, 0x7D
]

rcon = [0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1b, 0x36]

def xtime(a):
    high_bit = a >> 7
    result = (a << 1) & 0xff
    if high_bit:
        result ^= 0x1b
    return result

def gf_mult(a, b):
    p = 0
    for _ in range(8):
        if b & 1:
            p ^= a
        a = xtime(a)
        b >>= 1
    return p

def sub_bytes(state, inverse=False):
    box = inv_s_box if inverse else s_box
    for i in range(4):
        for j in range(4):
            state[i][j] = box[state[i][j]]
    return state

def shift_rows(state, inverse=False):
    shifted = [row[:] for row in state]
    for i in range(1,4):
        shift = i if not inverse else 4 - i
        shifted[i] = state[i][shift:] + state[i][:shift]
    return shifted

def mix_columns(state, inverse=False):
    new_state = [[0]*4 for _ in range(4)]
    for i in range(4):
        if inverse:
            s0 = gf_mult(0x0e, state[0][i]) ^ gf_mult(0x0b, state[1][i]) ^ gf_mult(0x0d, state[2][i]) ^ gf_mult(0x09, state[3][i])
            s1 = gf_mult(0x09, state[0][i]) ^ gf_mult(0x0e, state[1][i]) ^ gf_mult(0x0b, state[2][i]) ^ gf_mult(0x0d, state[3][i])
            s2 = gf_mult(0x0d, state[0][i]) ^ gf_mult(0x09, state[1][i]) ^ gf_mult(0x0e, state[2][i]) ^ gf_mult(0x0b, state[3][i])
            s3 = gf_mult(0x0b, state[0][i]) ^ gf_mult(0x0d, state[1][i]) ^ gf_mult(0x09, state[2][i]) ^ gf_mult(0x0e, state[3][i])
        else:
            s0 = gf_mult(0x02, state[0][i]) ^ gf_mult(0x03, state[1][i]) ^ state[2][i] ^ state[3][i]
            s1 = state[0][i] ^ gf_mult(0x02, state[1][i]) ^ gf_mult(0x03, state[2][i]) ^ state[3][i]
            s2 = state[0][i] ^ state[1][i] ^ gf_mult(0x02, state[2][i]) ^ gf_mult(0x03, state[3][i])
            s3 = gf_mult(0x03, state[0][i]) ^ state[1][i] ^ state[2][i] ^ gf_mult(0x02, state[3][i])
        new_state[0][i] = s0
        new_state[1][i] = s1
        new_state[2][i] = s2
        new_state[3][i] = s3
    return new_state

def add_round_key(state, round_key):
    for i in range(4):
        word = round_key[i]
        state[0][i] ^= (word >> 24) & 0xff
        state[1][i] ^= (word >> 16) & 0xff
        state[2][i] ^= (word >> 8) & 0xff
        state[3][i] ^= word & 0xff
    return state

def bytes_to_state(byte_array):
    state = [[0]*4 for _ in range(4)]
    for i in range(4):
        for j in range(4):
            state[j][i] = byte_array[i*4 + j]
    return state

def state_to_bytes(state):
    byte_array = bytearray(16)
    for i in range(4):
        for j in range(4):
            byte_array[i*4 + j] = state[j][i]
    return byte_array

def rot_word(word):
    return ((word << 8) & 0xffffffff) | (word >> 24)

def sub_word(word):
    return (s_box[(word >> 24) & 0xff] << 24) | \
           (s_box[(word >> 16) & 0xff] << 16) | \
           (s_box[(word >> 8) & 0xff] << 8) | \
           s_box[word & 0xff]

def key_expansion(key):
    nk = 4
    nr = 10
    w = [0] * (4 * (nr + 1))
    for i in range(nk):
        w[i] = (key[4*i] << 24) | (key[4*i+1] << 16) | (key[4*i+2] << 8) | key[4*i+3]
    for i in range(nk, 4*(nr+1)):
        temp = w[i-1]
        if i % nk == 0:
            temp = sub_word(rot_word(temp)) ^ (rcon[i//nk -1] << 24)
        w[i] = w[i - nk] ^ temp
    return w

def create_decryption_keys(w, nr=10):
    dw = list(w)
    for i in range(4, 4*nr):
        word = dw[i]
        s0 = (word >> 24) & 0xff
        s1 = (word >> 16) & 0xff
        s2 = (word >> 8) & 0xff
        s3 = word & 0xff
        t0 = gf_mult(0x0e, s0) ^ gf_mult(0x0b, s1) ^ gf_mult(0x0d, s2) ^ gf_mult(0x09, s3)
        t1 = gf_mult(0x09, s0) ^ gf_mult(0x0e, s1) ^ gf_mult(0x0b, s2) ^ gf_mult(0x0d, s3)
        t2 = gf_mult(0x0d, s0) ^ gf_mult(0x09, s1) ^ gf_mult(0x0e, s2) ^ gf_mult(0x0b, s3)
        t3 = gf_mult(0x0b, s0) ^ gf_mult(0x0d, s1) ^ gf_mult(0x09, s2) ^ gf_mult(0x0e, s3)
        dw[i] = (t0 << 24) | (t1 << 16) | (t2 << 8) | t3
    return dw

def print_state(state, title):
    print(f"{title}:")
    bytes = state_to_bytes(state)
    print(' '.join(f"{b:02x}" for b in bytes))
    print()

def print_round_key(round_key, title):
    print(f"{title}:")
    words = [f"{word:08x}" for word in round_key]
    print(' '.join(words))
    print()

def aes_encrypt(plaintext, key):
    state = bytes_to_state(plaintext)
    w = key_expansion(key)
    print("Encryption:")
    print_round_key(w[0:4], "Round 0 Key")
    state = add_round_key(state, w[0:4])
    print_state(state, "Round 0 Output")
    for r in range(1, 11):
        state = sub_bytes(state)
        state = shift_rows(state)
        if r != 10:
            state = mix_columns(state)
        round_key = w[r*4 : (r+1)*4]
        state = add_round_key(state, round_key)
        print_round_key(round_key, f"Round {r} Key")
        print_state(state, f"Round {r} Output")
    ciphertext = state_to_bytes(state)
    return ciphertext

def aes_decrypt(ciphertext, key):
    state = bytes_to_state(ciphertext)
    w = key_expansion(key)
    dw = create_decryption_keys(w)
    print("Decryption:")
    print_round_key(dw[40:44], "Round 0 Key")
    state = add_round_key(state, dw[40:44])
    print_state(state, "Round 0 Output")
    for r in range(9, 0, -1):
        state = sub_bytes(state, inverse=True)
        state = shift_rows(state, inverse=True)
        state = mix_columns(state, inverse=True)
        round_key = dw[r*4 : (r+1)*4]
        state = add_round_key(state, round_key)
        print_round_key(round_key, f"Round {10 - r} Key")
        print_state(state, f"Round {10 - r} Output")
    state = sub_bytes(state, inverse=True)
    state = shift_rows(state, inverse=True)
    state = add_round_key(state, dw[0:4])
    print_round_key(dw[0:4], "Round 10 Key")
    print_state(state, "Round 10 Output")
    plaintext = state_to_bytes(state)
    return plaintext

# Example usage:
plaintext = bytearray.fromhex("4d617468656d61746963733534333231")
key = bytearray.fromhex("4d617468656d61746963733132333435")

print("AES-128 Example:")
ciphertext = aes_encrypt(plaintext, key)
print("Ciphertext:", ciphertext.hex())

decrypted = aes_decrypt(ciphertext, key)
print("Decrypted:", decrypted.hex())
