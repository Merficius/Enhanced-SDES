from random import randint
from operator import xor


def generate_keys():
    # Permutation orders
    p10 = [2, 4, 1, 6, 3, 9, 0, 8, 7, 5]
    p8 = [5, 2, 6, 3, 7, 4, 9, 8]
    # Key generation
    key = []
    for i in range(0, 10):
        key.append(randint(0, 1))

    print(f"Random key generated: {key}")

    # P10
    key = [key[i] for i in p10]
    print(f"P10(K): {key}")

    # Obtention of 2 halves
    # First 5 items in key
    half_l = key[:5]
    # Last 5 items in list
    half_r = key[-5:]
    print(f"Left-half:1 {half_l}\nRight-half: {half_r}")

    # LS-1 for K1
    half_l = half_l[-4:] + half_l[:1]
    half_r = half_r[-4:] + half_r[:1]
    print(f"LS-1 of left-half: {half_l}\nLS-1 of right-half: {half_r}")

    # P8 of K1
    key1 = half_l + half_r
    key1 = [key1[i] for i in p8]
    print(f"P8(LS-1): {key1}")

    # LS-2 for K2
    half_l = half_l[-3:] + half_l[:2]
    half_r = half_r[-3:] + half_r[:2]
    print(f"LS-2 of left LS-1: {half_l}\nLS-2 of right LS-1: {half_r}")

    # P8 of K2
    key2 = half_l + half_r
    key2 = [key2[i] for i in p8]
    print(f"P8(LS-2): {key2}")

    print("------------------------------------------")
    print(f"Key-1: {key1}\nKey-2: {key2}")
    return (key1, key2)


def fk(ip, key1):
    ep = [3, 0, 1, 2, 1, 2, 3, 0]
    left_part = ip[:4]
    right_part = ip[-4:]
    expanded_right = [right_part[i] for i in ep]
    print(expanded_right)
    print(key1)
    for i in range(0, len(expanded_right)):
        expanded_right[i] = xor(expanded_right[i], key1[i])
    print(expanded_right)


# -----------------------------------------------------------------------
if __name__ == "__main__":
    ip = [1, 5, 2, 0, 3, 7, 4, 6]
    inverse_ip = [3, 0, 2, 4, 6, 1, 7, 5]
    key1, key2 = generate_keys()
    print("------------------------------------------")
    # Convert the 8-bit int message to a list
    original_message = int(input("Enter an 8-bit message: "))
    original_message = [int(x) for x in str(original_message)]
    # IP
    encrypted_message = [original_message[i] for i in ip]

    # fk
    fk(encrypted_message, key1)
