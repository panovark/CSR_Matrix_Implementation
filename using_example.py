from main import CSRMatrix


if __name__ == "__main__":
    print("\nA matrix: ")
    A = CSRMatrix(3, 3)
    A.insert(0, 0, 1)
    A.insert(1, 1, 1)
    A.insert(1, 1, 0)
    A.print_dense_from_csr()

    print("\nB matrix: ")
    B = CSRMatrix(3, 3)
    B.insert(0, 0, 1)
    B.insert(1, 1, 1)
    B.insert(2, 2, 1)
    B.print_dense_from_csr()

    print("\nValue from matrix A: ")
    print(A.get_value(0, 0))
    print(A.get_value(1, 0))

    print("\nVector: ")
    V = CSRMatrix(3, 1)
    V.insert(0, 0, 1)
    V.insert(1, 0, 1)
    V.insert(2, 0, 1)
    V.print_dense_from_csr()

    print("\nA * V: ")
    A.multiply_vector(V).print_dense_from_csr()

    print("\nA * B: ")
    A.multiply_matrix(B).print_dense_from_csr()

    print("\nA * 5: ")
    A.multiply_scalar(5).print_dense_from_csr()

    print("\nA + B: ")
    A.add_matrix(B).print_dense_from_csr()
