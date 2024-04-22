import config

from utils.algebra import int_to_bits, is_linearly_independent, gaussian_elimination_bit_strings, sdotx
# classical implementation of simons algorithm

# creating a function that takes n-bits and returns n-bits
# f(x) = f(x bitwise_XOR s)
# where s is a secret bit string
# domain of the function = {0, 1}^n
def f(x, s):
    # ^ is the bitwise XOR operator
    return x ^ s

# same as f above, but the inputs are both arrays of bits
def vector_f(x, s):
    return [x[i] ^ s[i] for i in range(len(x))]

# now, let's randomly choose an s
import random
# n = config.N_BITS
n = 6

s = random.randint(0, 2**n - 1)

print("Secret string s:" + bin(s)[2:].zfill(n))

# linearly independent bit strings
# we need n-1 linearly independent bit vectors
lin_indep = []

for i in range(2**n):
    res = int_to_bits(f(i, s), n)
    if is_linearly_independent(lin_indep + [res]):
        lin_indep.append(res)
    if len(lin_indep) == n - 1:
        break

if len(lin_indep) < n - 1:
    print(lin_indep)
    print("Could not find linearly independent bit strings.")
    exit(1)

# checking again that they are linearly independent
for vec1 in lin_indep:
    for vec2 in lin_indep:
        if vec1 == vec2:
            continue
        if not is_linearly_independent([vec1, vec2]):
            print("The vectors are not linearly independent.")
            exit(1)

print("Solving Ax = 0 using Gaussian elimination."
      "The first row of the result will be the secret string s.")

reduced = gaussian_elimination_bit_strings(lin_indep)
possible_s = reduced[0]
print("Possible secret string s:", possible_s)

error = False
for vec in lin_indep:
    vec_f = sdotx(vec, possible_s)
    if any(vec_f != 0 for i in range(n)):
        error = True
    print('{}.{} = {} (mod 2)'.format(vec, possible_s, vec_f))
if error:
    print("The possible secret string is incorrect.")
    exit(1)

print("The possible secret string is correct.")
