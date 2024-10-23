import unittest
from main import CSRMatrix


class TestCSRMatrix(unittest.TestCase):
    """Class for testing the functionality of the CSRMatrix class using the unittest module."""

    def setUp(self):
        """Initialize a 3x3 matrix before each test."""
        self.matrix = CSRMatrix(3, 3)

    def test_initialization(self):
        """Test to verify correct initialization of the CSR matrix."""
        self.assertEqual(self.matrix.num_rows, 3)
        self.assertEqual(self.matrix.num_cols, 3)
        self.assertEqual(self.matrix.values, [])
        self.assertEqual(self.matrix.col_indices, [])
        self.assertEqual(self.matrix.row_start, [0])

    def test_insert_and_get_value(self):
        """Test inserting values into the matrix and retrieving them using the get_value method."""
        self.matrix.insert(0, 0, 10)
        self.matrix.insert(1, 1, 20)
        self.matrix.insert(2, 2, 30)

        self.assertEqual(self.matrix.get_value(0, 0), 10)
        self.assertEqual(self.matrix.get_value(1, 1), 20)
        self.assertEqual(self.matrix.get_value(2, 2), 30)

        # Test retrieval of a value that doesn't exist
        self.assertEqual(self.matrix.get_value(0, 1), 0)
        self.assertEqual(self.matrix.get_value(1, 0), 0)

    def test_insert_replace_and_delete(self):
        """Test inserting a value, replacing it, and then deleting it by inserting zero."""
        self.matrix.insert(0, 0, 10)
        self.matrix.insert(0, 0, 15)  # Replace the value

        self.assertEqual(self.matrix.get_value(0, 0), 15)

        # Insert zero to delete the value
        self.matrix.insert(0, 0, 0)
        self.assertEqual(self.matrix.get_value(0, 0), 0)

    def test_matrix_vector_multiplication(self):
        """Test matrix-vector multiplication."""
        vector = CSRMatrix(3, 1)  # A vector of size 3x1
        vector.insert(0, 0, 1)
        vector.insert(1, 0, 2)
        vector.insert(2, 0, 3)

        self.matrix.insert(0, 0, 1)
        self.matrix.insert(1, 1, 2)
        self.matrix.insert(2, 2, 3)

        result = self.matrix.multiply_vector(vector)
        self.assertEqual(result.get_value(0, 0), 1)
        self.assertEqual(result.get_value(1, 0), 4)
        self.assertEqual(result.get_value(2, 0), 9)

    def test_matrix_addition(self):
        """Test addition of two matrices."""
        other = CSRMatrix(3, 3)
        self.matrix.insert(0, 0, 1)
        self.matrix.insert(1, 1, 2)
        self.matrix.insert(2, 2, 3)

        other.insert(0, 0, 4)
        other.insert(1, 1, 5)
        other.insert(2, 2, 6)

        result = self.matrix.add_matrix(other)
        self.assertEqual(result.get_value(0, 0), 5)
        self.assertEqual(result.get_value(1, 1), 7)
        self.assertEqual(result.get_value(2, 2), 9)

    def test_print_dense_from_csr(self):
        """Test printing the dense matrix representation from the CSR format."""
        self.matrix.insert(0, 0, 1)
        self.matrix.insert(0, 1, 2)
        self.matrix.insert(1, 2, 3)

        # Capture printed output
        import io
        import sys
        captured_output = io.StringIO()
        sys.stdout = captured_output
        self.matrix.print_dense_from_csr()
        sys.stdout = sys.__stdout__

        # Verify the dense matrix format
        expected_output = "1 2 0\n0 0 3\n0 0 0\n"
        self.assertEqual(captured_output.getvalue(), expected_output)


# Execute the test cases
if __name__ == "__main__":
    unittest.main()
