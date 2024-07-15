'''
Description: A module that extracts numbers from a text and calculates the sum of the profit.
'''

from typing import Generator


def generator_numbers(text: str) -> Generator[float, None, None]:
    """
    Extract numbers from the text.

    Parameters:
    - text (str): The text to extract numbers from.

    Yields:
    - float: The extracted number.
    """
    if isinstance(text, str) and text:
        for word in text.split():
            try:
                yield float(word)
            except ValueError:
                pass


def sum_profit(text: str, func: callable = generator_numbers) -> float:
    """
    Calculate the sum of the profit.

    Parameters:
    - text (str): The text to extract numbers from.
    - func (callable): The function to extract numbers from the text.

    Returns:
    - float: The sum of the profit.
    """
    return sum(profit for profit in func(text)) or 0
