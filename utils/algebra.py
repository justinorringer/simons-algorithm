import numpy as np
def int_to_bits(x, num_bits):
    print(x)
    # Convert the integer to a binary string and pad with zeros
    binary_str = bin(x)[2:].zfill(num_bits)

    # Convert the binary string to a list of bits
    bits = [int(bit) for bit in binary_str]

    print(bits)
    return bits

def is_linearly_independent(vectors):
    matrix = np.array(vectors)
    rank = np.linalg.matrix_rank(matrix, tol=None)
    return rank == matrix.shape[1]

def gaussian_elimination_bit_strings(set):
    """Perform Gaussian elimination on a matrix of bit strings."""
    matrix = np.array(set)
    rows, cols = matrix.shape
    row = 0
    for col in range(cols):
        if row >= rows:
            break
        if matrix[row][col] == 0:
            nonzero_row = row + 1
            while nonzero_row < rows and matrix[nonzero_row, col] == 0:
                nonzero_row += 1
            if nonzero_row == rows:
                continue
            matrix[[row, nonzero_row]] = matrix[[nonzero_row, row]]
        pivot = matrix[row, col]
        if pivot != 0:
            matrix[row] //= pivot
            for i in range(row + 1, rows):
                factor = matrix[i, col]
                if factor != 0:
                    matrix[i] ^= matrix[row] & factor
            row += 1
    return matrix

# Calculate the dot product of the results
def sdotx(s, x):
    accum = 0
    for i in range(len(s)):
        accum += int(s[i]) * int(x[i])
    return (accum % 2)
