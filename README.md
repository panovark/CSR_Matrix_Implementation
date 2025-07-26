
# CSRMatrix

## Overview

This project provides a Python implementation of the Compressed Sparse Row (CSR) matrix data structure, enabling efficient storage and manipulation of large, sparse matrices. The core functionality is encapsulated in the `CSRMatrix` class, which supports insertion, retrieval, arithmetic operations, and dense-format output of sparse matrices.

## Features

- **Matrix Construction**: Create sparse matrices of any size.
- **Insertion & Update**: Add or update non-zero elements at specified positions; inserting a zero deletes the element.
- **Value Retrieval**: Efficiently fetch any element, returning 0 for positions without stored values.
- **Vector & Matrix Operations**:
  - Scalar multiplication
  - Matrix-vector multiplication
  - Matrix-matrix multiplication
  - Element-wise matrix addition
- **Vector Check**: Determine if a matrix represents a vector (single column).
- **Dense Output**: Convert and print the sparse representation in standard dense (2D) format.
- **Unit Testing**: Comprehensive test suite covering initialization, insertion, retrieval, replacement and deletion of zeros, scalar multiplication, matrix-vector and matrix-matrix multiplication, matrix addition, and dense-format output.

## Project Structure

```
.
├── main.py             # Implements the CSRMatrix class and its methods.
├── tests.py            # Contains unittest cases to validate all functionality.
└── using_example.py    # Demonstrates typical usage scenarios and prints results to the console.
```

> *Note: Ensure all files are located in the same directory before running any scripts.*

## Requirements

- Python 3.6 or higher  
- No external dependencies (uses only Python’s standard library)

## Installation & Setup

1. Clone or download the repository into a single folder.  
2. (Optional) Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. No additional packages are required.

## Usage

### Running the Example Script

```bash
python using_example.py
```

This will:

1. Create and populate a few sample matrices and a vector.  
2. Display each in dense format.  
3. Perform and display results of scalar multiplication, matrix-vector and matrix-matrix multiplication, and matrix addition.

### API Reference

Below is a summary of the `CSRMatrix` class methods:

- `CSRMatrix(num_rows: int, num_cols: int)`
  - Initialize an empty CSR matrix with the given dimensions.

- `insert(row: int, col: int, value: float) -> None`
  - Insert, update, or delete (if `value==0`) a non-zero element. Raises `ValueError` if indices are out of bounds.

- `get_value(row: int, col: int) -> float`
  - Retrieve the value at `(row, col)`, returning 0.0 if not explicitly stored.

- `is_vector() -> bool`
  - Returns `True` if the matrix has exactly one column.

- `multiply_scalar(scalar: float) -> CSRMatrix`
  - Returns a new CSR matrix scaled by the given scalar.

- `multiply_vector(vector: CSRMatrix) -> CSRMatrix`
  - Multiplies the matrix by a vector (CSR with one column). Raises `ValueError` if dimensions mismatch or operand is not a vector.

- `multiply_matrix(other: CSRMatrix) -> CSRMatrix`
  - Matrix-matrix multiplication. Raises `ValueError` on dimension mismatch.

- `add_matrix(other: CSRMatrix) -> CSRMatrix`
  - Element-wise addition of two matrices. Raises `ValueError` if dimensions differ.

- `print_dense_from_csr() -> None`
  - Converts the sparse matrix to dense form and prints it row by row.

## Example

```python
from main import CSRMatrix

# Create a 3x3 identity matrix
I = CSRMatrix(3, 3)
for i in range(3):
    I.insert(i, i, 1)

# Print dense representation
I.print_dense_from_csr()
# Output:
# 1 0 0
# 0 1 0
# 0 0 1
```

## Running Tests

Execute the test suite to verify correctness of all operations, including insertion, update, deletion via zero insertion, scalar multiplication, matrix-vector and matrix-matrix multiplication, addition, and dense-format output:

```bash
python -m unittest tests.py
```

## 📄 License

[MIT](LICENSE) © 2025 Arkadiy Panov
