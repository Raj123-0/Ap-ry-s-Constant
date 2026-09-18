from __future__ import annotations
"""Module for mathematical computation and analysis."""


import functools
import math
import multiprocessing as mp
import sys


def compute_chunk_bs(args):
    """Compute chunk bs using optimized algorithms.
    
    Args:
        args:
    
    Returns:
        The computed result
    
    """
    start, end = args
    return binary_split_range(start, end)


@functools.lru_cache(maxsize=None)
def binary_split_range(a, b) -> tuple:
    """Binary split range.
    
    Args:
        a:
        b:
    
    Returns:
        tuple: Result of type tuple
    
    """
    if a == b:
        if a == 1:
            P = 1
            Q = 32
        else:
            P = -((a - 1) ** 5)
            Q = 32 * (2 * a - 1) ** 5
        T = P * (205 * a * a - 160 * a + 32)
        return P, Q, T
    
    m = (a + b) // 2
    P1, Q1, T1 = binary_split_range(a, m)
    P2, Q2, T2 = binary_split_range(m + 1, b)
    
    P = P1 * P2
    Q = Q1 * Q2
    T = T1 * Q2 + P1 * T2
    return P, Q, T


def main():
    """Entry point — parse arguments and run the main computation.
    
    """
    if len(sys.argv) > 1:
        try:
            N = int(sys.argv[1])
        except ValueError:
            print("Number of digits must be an integer.")
            sys.exit(1)
        if N <= 0:
            print("Number of digits must be positive.")
            sys.exit(1)
    else:
        while True:
            try:
                N_input = input("Enter the number of digits to calculate: ")
                N = int(N_input)
                if N > 0:
                    break
                else:
                    print("Please enter a positive integer.")
            except ValueError:
                print("Invalid input. Please enter a valid integer.")
        
    # Python 3.11+ limit for converting large integers to strings
    try:
        sys.set_int_max_str_digits(0)
    except AttributeError:
        pass
        
    constant_name = "Apéry's Constant"
    
    # Calculate required number of mathematical terms (AZ series converges at ~3.01 digits per term)
    K = int(math.ceil(N / 3.0102999566)) + 5
    
    target_threads = mp.cpu_count()
    num_chunks = target_threads
    
    if K < num_chunks * 10:
        num_chunks = 1
        
    chunks = []
    if num_chunks == 1:
        chunks = [(1, K)]
    else:
        chunk_size = K // num_chunks
        for i in range(num_chunks):
            start = i * chunk_size + 1
            end = K if i == num_chunks - 1 else (i + 1) * chunk_size
            chunks.append((start, end))
            
    print(f"Calculating {constant_name} to {N} significant digits...")
    print(f"Target Terms: {K} | Worker Threads: {target_threads}")
    
    if num_chunks > 1:
        # Execute in parallel
        with mp.Pool(processes=target_threads) as pool:
            results = pool.map(compute_chunk_bs, chunks)
            
        P_total, Q_total, T_total = results[0]
        for P, Q, T in results[1:
            ]:
            T_total = T_total * Q + P_total * T
            P_total = P_total * P
            Q_total = Q_total * Q
    else:
        P_total, Q_total, T_total = binary_split_range(1, K)
        
    # The formula is Zeta(3) = (1/2) * (T / Q)
    # To get N decimal digits, we multiply by 10**(N + 10) and integer divide by 2*Q
    # Then we truncate to N characters.
    print("Performing final high-precision division (integer arithmetic)...")
    val = (T_total * 10**(N + 10)) // (2 * Q_total)
    str_val = str(val)[:N]
    
    continuous_filename = f"{constant_name}_{N}_digits.txt"
    bfile_filename = f"b_{constant_name}.txt"
    
    # Write the continuous unspaced string
    try:
        with open(continuous_filename, "w", encoding="utf-8") as f:
            f.write(str_val + "\n")
        print(f"Continuous digits written to: {continuous_filename}")
    except IOError:
        print(f"Error opening {continuous_filename} for writing.")
        
    # Write the strictly formatted OEIS B-file
    try:
        with open(bfile_filename, "w", encoding="utf-8") as f:
            for i in range(N):
                f.write(f"{i + 1} {str_val[i]}\n")
        print(f"B-file generated at: {bfile_filename}")
    except IOError:
        print(f"Error opening {bfile_filename} for writing.")

if __name__ == "__main__":
    # Freeze support is needed if building an executable on Windows
    mp.freeze_support()
    main()
