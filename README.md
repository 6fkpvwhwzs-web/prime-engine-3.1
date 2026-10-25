# Prime Engine 3.1 - Cuban Primes Sieve

A highly optimized, deterministic index sieve for numbers of the form `H(n) = 3n^2 + 3n + 1` (cuban primes). 
It uses pure Python (standard library only) with no probabilistic tests (no Miller-Rabin).

## Performance
Benchmark on iPhone (Jupyter/Carnets, Python 3.13, ~4 GB RAM):
- `n = 100,000,000`: Finds **9,389,636 primes** in **21.26 seconds**.
- `n = 50,000,000`: Finds 4,884,891 primes in ~20 seconds.

## How it works
Instead of testing values `H(n)` for primality, this engine sieves the indices `n`. 
It leverages the fact that for any prime `p ≡ 1 (mod 3)`, the equation `H(n) ≡ 0 (mod p)` has exactly two roots. 
The code uses a cubic root of unity modulo `p` to find these roots instantly, and uses C-level `bytearray` slice assignments to clear out composite indices rapidly.
