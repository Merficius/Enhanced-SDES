from random import randint
from operator import xor

IP = [1, 5, 2, 0, 3, 7, 4, 6]
INVERSE_IP = [3, 0, 2, 4, 6, 1, 7, 5]


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


def fk(ip, key):
    expansion_permutation = [3, 0, 1, 2, 1, 2, 3, 0]
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

    expanded_right = [right_part[i] for i in expansion_permutation]
    print("Expanded right:", expanded_right)
    print("Key:", key)

    # xor between key and e/p
    for i in range(0, len(expanded_right)):
        expanded_right[i] = xor(expanded_right[i], key[i])
    print("expanded right after xor:", expanded_right)

    # Declaration of bits
    p00 = str(expanded_right[0])
    p03 = str(expanded_right[3])
    p01 = str(expanded_right[1])
    p02 = str(expanded_right[2])
    p10 = str(expanded_right[4])
    p13 = str(expanded_right[7])
    p11 = str(expanded_right[5])
    p12 = str(expanded_right[6])

    # Concat values and cast them to int to access s boxes
    s0_output = s0[int(p00 + p03, 2)][int(p01 + p02, 2)]
    s1_output = s1[int(p10 + p13, 2)][int(p11 + p12, 2)]
    print("s0 output =", s0_output)
    print("s1 output =", s1_output)

    s0s1 = map_decimal_to_binary_array(
        s0_output) + map_decimal_to_binary_array(s1_output)
    print("s0s1 =", s0s1)
    permuted_s0s1 = [s0s1[i] for i in p4]
    print("result after p4=", permuted_s0s1)

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
    key1, key2 = generate_keys()
    #key1 = [1, 0, 1, 0, 0, 1, 0, 0]
    #key2 = [0, 1, 0, 0, 0, 0, 1, 1]
    print("key1 =", key1)
    print("key2 =", key2)

    # Convert the 8-bit int message to a list
    original_message = input("Enter an 8-bit message: ")
    original_message = [int(x) for x in original_message]
    #original_message = [1, 0, 1, 1, 1, 1, 0, 1]

    # Simple Columnar Transposition Technique
    sctt_first_round = original_message[6:] + \
        original_message[:3] + original_message[3:6]
    print("SCTT after first round:", sctt_first_round)
    sctt_second_round = sctt_first_round[6:] + \
        sctt_first_round[:3] + sctt_first_round[3:6]
    print("SCTT after second round:", sctt_second_round)

    '''
    Shift rows
    0 1 
    2 3 4
    5 6 7

    0 1
    3 4 2
    7 5 6'''
    shift = [0, 1, 3, 4, 2, 7, 5, 6]
    es_des_output = [sctt_second_round[i] for i in shift]
    print("<<<<<<<<<<<<<<<<<<<<<<es_des_ouput=", es_des_output)

    # First round
    first_round_input = [es_des_output[i] for i in IP]
    print("encryped message after initial permutation:", first_round_input)
    first_round_result = fk(first_round_input, key1)
    print("Left result (first round) =", first_round_result)

    # Second round
    second_round_input = first_round_input[-4:] + first_round_result
    print("second round input:", second_round_input)
    second_round_result = fk(second_round_input, key2)
    print("second round result:", second_round_result)

    # Final result
    final_result = second_round_result + first_round_result
    final_result_permuted = [final_result[i] for i in INVERSE_IP]
    print("final_result_permuted =", final_result_permuted)

    # Decryption
    print("\n------------------DECRYPTION------------------\n")
    # First round
    first_round_input = [final_result_permuted[i] for i in IP]
    print("decrypted message after initial permutation:", first_round_input)
    first_round_result = fk(first_round_input, key2)
    print("Left result (first round) =", first_round_result)

    # Second round
    second_round_input = first_round_input[-4:] + first_round_result
    print("second round input:", second_round_input)
    second_round_result = fk(second_round_input, key1)
    print("second round result:", second_round_result)

    # Final result simplified des
    final_result = second_round_result + first_round_result
    final_result_permuted = [final_result[i] for i in INVERSE_IP]
    print("final_result_permuted =", final_result_permuted)

    # Inverse shift rows
    '''
    Shift rows
    0 1 
    2 3 4
    5 6 7

    0 1
    4 2 3
    6 7 5'''
    inverse_shift = [0, 1, 4, 2, 3, 6, 7, 5]
    inverse_shift_output = [final_result_permuted[i] for i in inverse_shift]
    print("<<<<<<<<<<<<<<<<<<<<<<inverse shift output=", inverse_shift_output)

    # Simple Columnar Transposition Technique
    sctt_first_round = inverse_shift_output[6:] + \
        inverse_shift_output[:3] + inverse_shift_output[3:6]
    print("SCTT after first round:", sctt_first_round)
    sctt_second_round = sctt_first_round[6:] + \
        sctt_first_round[:3] + sctt_first_round[3:6]
    print("plaintext:", sctt_second_round)
