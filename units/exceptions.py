class OperationError(Exception):
    def __init__(self, operation, left, right):
        self.operation = operation
        self.left = left
        self.right = right

    def __str__(self):
        return f"Cannot {self.operation} {self.left} to {self.right}"
