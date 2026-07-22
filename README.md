===============================================================================
PROJECT: Apéry's Constant Computation Engine
===============================================================================

OVERVIEW:
Calculates Apéry's constant (zeta(3) ≈ 1.202056903159594...) to N significant digits.

ALGORITHM & IMPLEMENTATION:
- Amdeberhan-Zeilberger Series: Uses rapidly converging hypergeometric series 
  providing ~3.01 decimal digits of precision per evaluated mathematical term.
- Parallel Binary Splitting: Employs a divide-and-conquer binary split tree 
  parallelized across CPU cores using multiprocessing to aggregate large 
  integer numerators and denominators without memory bottlenecks.
