class CSRMatrix:
    def __init__(self, num_rows, num_cols):
        """
        Initialize a Compressed Sparse Row (CSR) matrix.

        Parameters:
        num_rows (int): The number of rows in the matrix.
        num_cols (int): The number of columns in the matrix.
        """
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.values = []  # Non-zero values of the matrix
        self.col_indices = []  # Column indices of the non-zero values
        self.row_start = [0]  # Cumulative counts of non-zero values for each row

    def insert(self, row, col, value):
        """
        Insert or update a value in the matrix at the specified row and column.

        Parameters:
        row (int): The row index of the value to insert.
        col (int): The column index of the value to insert.
        value (float): The value to insert.

        Raises:
        ValueError: If the specified row or column index is out of bounds.
        """
        if row < 0 or row >= self.num_rows or col < 0 or col >= self.num_cols:
            raise ValueError("Row or column index out of bounds.")

        # Extend row_start if necessary
        while len(self.row_start) <= row + 1:
            self.row_start.append(self.row_start[-1])

        row_start = self.row_start[row]
        row_end = self.row_start[row + 1]

        # Update existing value if present
        for i in range(row_start, row_end):
            if self.col_indices[i] == col:
                if value == 0:
                    # Remove the entry if the value is 0
                    del self.values[i]
                    del self.col_indices[i]
                    for j in range(row + 1, len(self.row_start)):
                        self.row_start[j] -= 1
                else:
                    self.values[i] = value
                return

        # If value is 0, do nothing
        if value == 0:
            return

        # Find the position to insert the new value
        insert_pos = row_end
        for i in range(row_start, row_end):
            if self.col_indices[i] > col:
                insert_pos = i
                break

        # Insert the new value and column index
        self.values.insert(insert_pos, value)
        self.col_indices.insert(insert_pos, col)
        for i in range(row + 1, len(self.row_start)):
            self.row_start[i] += 1

    def get_value(self, row, col):
        """
        Retrieve the value at the specified row and column.

        Parameters:
        row (int): The row index of the value to retrieve.
        col (int): The column index of the value to retrieve.

        Returns:
        float: The value at the specified row and column, or 0 if not found.

        Raises:
        ValueError: If the specified row or column index is out of bounds.
        """
        if row < 0 or row >= self.num_rows or col < 0 or col >= self.num_cols:
            raise ValueError("Row or column index out of bounds.")

        row_start = self.row_start[row]
        row_end = self.row_start[row + 1] if row + 1 < len(self.row_start) else len(self.values)
        for i in range(row_start, row_end):
            if self.col_indices[i] == col:
                return self.values[i]
        return 0

    def is_vector(self):
        """
        Check if the matrix is a vector (single column).

        Returns:
        bool: True if the matrix is a vector, False otherwise.
        """
        return self.num_cols == 1

    def multiply_vector(self, vector):
        """
        Multiply the matrix by a vector.

        Parameters:
        vector (CSRMatrix): The vector to multiply with.

        Returns:
        CSRMatrix: The resulting vector after multiplication.

        Raises:
        ValueError: If the argument is not a vector or dimensions do not match.
        """
        if not vector.is_vector():
            raise ValueError("The argument is not a vector.")
        if vector.num_rows != self.num_cols:
            raise ValueError("The size of the vector and size of the matrix are not the same")

        result_values = []
        result_col_indices = []
        result_row_start = [0]

        for i in range(self.num_rows):
            row_result = 0
            row_start = self.row_start[i]
            row_end = self.row_start[i + 1] if i + 1 < len(self.row_start) else len(self.values)
            for j in range(row_start, row_end):
                row_result += self.values[j] * vector.get_value(self.col_indices[j], 0)
            if row_result != 0:
                result_values.append(row_result)
                result_col_indices.append(0)
            result_row_start.append(len(result_values))

        result = CSRMatrix(self.num_rows, 1)
        result.values = result_values
        result.col_indices = result_col_indices
        result.row_start = result_row_start
        return result

    def multiply_matrix(self, other):
        """
        Multiply the matrix by another matrix.

        Parameters:
        other (CSRMatrix): The matrix to multiply with.

        Returns:
        CSRMatrix: The resulting matrix after multiplication.

        Raises:
        ValueError: If matrix dimensions are incompatible for multiplication.
        """
        if self.num_cols != other.num_rows:
            raise ValueError("Incompatible matrix dimensions for multiplication.")

        result_values = []
        result_col_indices = []
        result_row_start = [0]

        for i in range(self.num_rows):
            row_dict = {}
            row_start = self.row_start[i]
            row_end = self.row_start[i + 1] if i + 1 < len(self.row_start) else len(self.values)
            for j in range(row_start, row_end):
                col = self.col_indices[j]
                value = self.values[j]
                other_row_start = other.row_start[col]
                other_row_end = other.row_start[col + 1] if col + 1 < len(other.row_start) else len(other.values)
                for k in range(other_row_start, other_row_end):
                    other_col = other.col_indices[k]
                    if other_col in row_dict:
                        row_dict[other_col] += value * other.values[k]
                    else:
                        row_dict[other_col] = value * other.values[k]

            for col, value in row_dict.items():
                if value != 0:
                    result_values.append(value)
                    result_col_indices.append(col)
            result_row_start.append(len(result_values))

        result = CSRMatrix(self.num_rows, other.num_cols)
        result.values = result_values
        result.col_indices = result_col_indices
        result.row_start = result_row_start
        return result

    def multiply_scalar(self, scalar):
        """
        Multiply the matrix by a scalar.

        Parameters:
        scalar (float): The scalar to multiply with.

        Returns:
        CSRMatrix: The resulting matrix after multiplication.
        """
        if scalar == 0:
            return CSRMatrix(self.num_rows, self.num_cols)

        result_values = [value * scalar for value in self.values]
        result_col_indices = self.col_indices[:]
        result_row_start = self.row_start[:]

        result = CSRMatrix(self.num_rows, self.num_cols)
        result.values = result_values
        result.col_indices = result_col_indices
        result.row_start = result_row_start
        return result

    def add_matrix(self, other):
        """
        Add another matrix to this matrix.

        Parameters:
        other (CSRMatrix): The matrix to add.

        Returns:
        CSRMatrix: The resulting matrix after addition.

        Raises:
        ValueError: If matrix dimensions do not match.
        """
        if self.num_rows != other.num_rows or self.num_cols != other.num_cols:
            raise ValueError("Matrix dimensions must match for addition.")

        result_values = []
        result_col_indices = []
        result_row_start = [0]

        for i in range(self.num_rows):
            row_dict = {}
            row_start = self.row_start[i]
            row_end = self.row_start[i + 1] if i + 1 < len(self.row_start) else len(self.values)
            for j in range(row_start, row_end):
                row_dict[self.col_indices[j]] = self.values[j]
            other_row_start = other.row_start[i]
            other_row_end = other.row_start[i + 1] if i + 1 < len(other.row_start) else len(other.values)
            for j in range(other_row_start, other_row_end):
                if other.col_indices[j] in row_dict:
                    row_dict[other.col_indices[j]] += other.values[j]
                else:
                    row_dict[other.col_indices[j]] = other.values[j]

            for col, value in row_dict.items():
                if value != 0:
                    result_values.append(value)
                    result_col_indices.append(col)
            result_row_start.append(len(result_values))

        result = CSRMatrix(self.num_rows, self.num_cols)
        result.values = result_values
        result.col_indices = result_col_indices
        result.row_start = result_row_start
        return result

    def print_dense_from_csr(self):
        """
        Prints the matrix in dense format.

        This method converts the sparse matrix represented in CSR format
        into a dense format and prints it to the console.

        Returns:
            None
        """
        result = ""
        for i in range(self.num_rows):
            row_dict = {}
            row_start = self.row_start[i]
            row_end = self.row_start[i + 1] if i + 1 < len(self.row_start) else len(self.values)
            for j in range(row_start, row_end):
                row_dict[self.col_indices[j]] = self.values[j]
            row_result = " ".join(str(row_dict.get(col, 0)) for col in range(self.num_cols))
            result += row_result + "\n"

        print(result.strip())
