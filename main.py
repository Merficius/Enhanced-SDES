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
    p4 = [1, 3, 2, 0]
    s0 = [[1, 0, 3, 2],
          [3, 2, 1, 0],
          [0, 2, 1, 3],
          [3, 1, 3, 2]]
    s1 = [[0, 1, 2, 3],
          [2, 0, 1, 3],
          [3, 0, 1, 0],
          [2, 1, 0, 3]]
    left_part = ip[:4]
    right_part = ip[-4:]
    expanded_right = [right_part[i] for i in ep]
    print(expanded_right)
    print(key1)
    for i in range(0, len(expanded_right)):
        expanded_right[i] = xor(expanded_right[i], key1[i])
    p00 = str(expanded_right[0])
    p03 = str(expanded_right[3])
    p01 = str(expanded_right[1])
    p02 = str(expanded_right[2])
    p10 = str(expanded_right[4])
    p13 = str(expanded_right[7])
    p11 = str(expanded_right[5])
    p12 = str(expanded_right[6])
    print(expanded_right)

    # Concat values and cast them to int to access s boxes
    s0_output = s0[int(p00 + p03, 2)][int(p01 + p02, 2)]
    s1_output = s1[int(p10 + p13, 2)][int(p11 + p12, 2)]
    print("s0 output =", s0_output)
    print("s1 output =", s1_output)

    s0s1 = map_decimal_to_binary_array(s0_output) + map_decimal_to_binary_array(s1_output)
    print("s0s1 =", s0s1)
    permuted_s0s1 = [s0s1[i] for i in p4]
    print("permuted result =", permuted_s0s1)

    result = []
    print(left_part, permuted_s0s1)
    for i in range(0, len(left_part)):
        result.append(xor(left_part[i], permuted_s0s1[i]))

    return result



def map_decimal_to_binary_array(decimal_value):
    if decimal_value == 0:
        return [0, 0]
    elif decimal_value == 1:
        return [0, 1]
    elif decimal_value == 2:
        return [1, 0]
    elif decimal_value == 3:
        return [1, 1]   


# -----------------------------------------------------------------------
if __name__ == "__main__":
    ip = [1, 5, 2, 0, 3, 7, 4, 6]
    inverse_ip = [3, 0, 2, 4, 6, 1, 7, 5]
    key1, key2 = generate_keys()
    #delete
    key1 = [1, 0, 1, 0, 0, 1, 0, 0]
    key2 = [0, 1, 0, 0, 0, 0, 1, 1]
    
    print("------------------------------------------")
    # Convert the 8-bit int message to a list
    original_message = input("Enter an 8-bit message: ")
    original_message = [int(x) for x in str(original_message)]
    # IP
    original_message = [1, 0, 1, 1, 1, 1, 0, 1]#delete
    encrypted_message = [original_message[i] for i in ip]
    print("encryped message:", encrypted_message)
    # fk
    first_result = fk(encrypted_message, key1)
    encrypted_message_2 = encrypted_message[-4:] + first_result
    print("first_result:", first_result)
    print("encrypted message 2:", encrypted_message_2)
    second_result = fk(encrypted_message_2, key2)
    print("second result:", second_result)

    final_result = second_result + first_result
    final_result_permuted = [final_result[i] for i in inverse_ip]
    print("final_result_permuted =", final_result_permuted)
