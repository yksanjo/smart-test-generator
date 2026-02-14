"""Sample Calculator Module - For testing the Smart Test Generator."""


def add(a: int, b: int) -> int:
    """Add two numbers.
    
    Args:
        a: First number
        b: Second number
        
    Returns:
        Sum of a and b
    """
    return a + b


def subtract(a: int, b: int) -> int:
    """Subtract b from a.
    
    Args:
        a: First number
        b: Second number
        
    Returns:
        Difference of a and b
    """
    return a - b


def multiply(a: int, b: int) -> int:
    """Multiply two numbers.
    
    Args:
        a: First number
        b: Second number
        
    Returns:
        Product of a and b
    """
    return a * b


def divide(a: int, b: int) -> float:
    """Divide a by b.
    
    Args:
        a: First number
        b: Second number
        
    Returns:
        Quotient of a and b
        
    Raises:
        ZeroDivisionError: If b is zero
    """
    if b == 0:
        raise ZeroDivisionError("Cannot divide by zero")
    return a / b


def process_data(data: list) -> dict:
    """Process a list of data.
    
    Args:
        data: List of numbers
        
    Returns:
        Dictionary with processing results
    """
    if not data:
        return {"sum": 0, "average": 0, "count": 0}
    
    return {
        "sum": sum(data),
        "average": sum(data) / len(data),
        "count": len(data),
        "min": min(data),
        "max": max(data)
    }


class Calculator:
    """A simple calculator class."""
    
    def __init__(self, initial_value: int = 0):
        """Initialize calculator.
        
        Args:
            initial_value: Starting value
        """
        self.value = initial_value
        
    def add(self, n: int) -> int:
        """Add n to the current value.
        
        Args:
            n: Number to add
            
        Returns:
            New value
        """
        self.value += n
        return self.value
    
    def subtract(self, n: int) -> int:
        """Subtract n from the current value.
        
        Args:
            n: Number to subtract
            
        Returns:
            New value
        """
        self.value -= n
        return self.value
    
    def get_value(self) -> int:
        """Get current value.
        
        Returns:
            Current value
        """
        return self.value
    
    def reset(self) -> None:
        """Reset calculator to zero."""
        self.value = 0


def validate_input(value: str) -> bool:
    """Validate user input.
    
    Args:
        value: Input string to validate
        
    Returns:
        True if valid, False otherwise
    """
    if not value:
        return False
    return value.isdigit()


def encode_data(data: str) -> str:
    """Encode data (simple base64 simulation).
    
    Args:
        data: String to encode
        
    Returns:
        Encoded string
    """
    import base64
    return base64.b64encode(data.encode()).decode()


def decode_data(data: str) -> str:
    """Decode data.
    
    Args:
        data: Encoded string
        
    Returns:
        Decoded string
    """
    import base64
    return base64.b64decode(data.encode()).decode()
