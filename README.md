# Polynomial Secret Finder

This project implements a solution for finding the constant term 'c' of a polynomial using Shamir's Secret Sharing algorithm with Lagrange interpolation.

## Problem Statement

Given a polynomial of degree m:
```
f(x) = a_m x^m + a_{m-1} x^{m-1} + ... + a_1 x + c
```

The task is to find the constant term 'c' using k points (where k = m + 1) from n total points provided in a specific JSON format.

## Input Format

The input is provided in JSON format with the following structure:

```json
{
    "keys": {
        "n": 4,        
        "k": 3        
    },
    "1": {
        "base": "10",  
        "value": "4"   
    },
    "2": {
        "base": "2",
        "value": "111"
    }
    
}
```

### Point Decoding

Each point is represented as (x, y) where:
- x is the key of the object
- y is decoded from the "value" field using the specified "base"

Example: `"2": {"base": "2", "value": "111"}` becomes point (2, 7) because 111 in base 2 = 7.

## Solution Approach

1. **JSON Parsing**: Read and parse the input JSON file
2. **Base Decoding**: Convert encoded values to decimal using the specified base
3. **Combination Generation**: Generate all possible combinations of k points from n points
4. **Lagrange Interpolation**: Use Lagrange interpolation to find the constant term for each combination
5. **Consensus Detection**: Find the most frequently occurring constant term as the correct answer

## Algorithm Details

### Lagrange Interpolation

The algorithm uses Lagrange interpolation to reconstruct the polynomial:

```
P(x) = Σ(y_i * L_i(x))
```

Where L_i(x) are the Lagrange basis polynomials.

### Modular Arithmetic

The implementation uses modular arithmetic with a large prime (2^256 - 189) to handle large numbers and ensure numerical stability.

## Files

- `solution.js` - Main implementation
- `testcase1.json` - First test case
- `testcase2.json` - Second test case
- `README.md` - This documentation

## Usage

```bash
# Run the solution
node solution.js
```

## Output

The program will output:
- Decoded points from the JSON input
- All combinations of k points
- Constant term found for each combination
- Final consensus result (the secret)

## Example Output

```
=== POLYNOMIAL SECRET FINDER ===
Polynomial degree: 2
Required points: 3
Total points provided: 4

Point 1: (1, 4) [decoded from base 10: "4"]
Point 2: (2, 7) [decoded from base 2: "111"]
Point 3: (3, 12) [decoded from base 10: "12"]
Point 6: (6, 39) [decoded from base 4: "213"]

=== FINDING CONSTANT TERM ===
Using 3 points to interpolate polynomial of degree 2
Generated 4 combinations of 3 points

🎯 FINAL ANSWER: [constant_term_value]
```

## Mathematical Foundation

The solution is based on the fact that a polynomial of degree m can be uniquely determined by m+1 points. Using Lagrange interpolation, we can reconstruct the polynomial and extract the constant term.

## Constraints

- All coefficients are positive integers
- Coefficients are within 256-bit range
- n ≥ k (more points provided than required)
- Degree m = k - 1

## Error Handling

The implementation includes robust error handling for:
- Invalid base conversions
- Modular inverse failures
- Invalid combinations
- File reading errors

## Performance

- Time Complexity: O(C(n,k) * k²) for interpolation
- Space Complexity: O(C(n,k) * k) for storing combinations
- Optimized for large number arithmetic using BigInt 