"""
Data Processing Utilities
"""

import html

def calculate_average(numbers):
    """Calculate the average of a list of numbers"""
    if not numbers:
        raise ValueError("numbers must not be empty")
    return sum(numbers) / len(numbers)


def filter_data(data, threshold):
    """Filter data above a certain threshold"""
    result = []
    for item in data:
        if item > threshold:
            result.append(item)
    return result


def process_user_data(users):
    """Process user data and return statistics"""
    # Build filtered ages list, extracting only valid age values
    ages = []
    for user in users:
        if 'age' in user and isinstance(user['age'], (int, float)):
            ages.append(user['age'])

    # Handle empty ages list
    if not ages:
        return {
            'average_age': None,
            'oldest': None,
            'youngest': None,
            'total_users': len(users)
        }

    avg_age = calculate_average(ages)

    return {
        'average_age': avg_age,
        'oldest': max(ages),
        'youngest': min(ages),
        'total_users': len(users)
    }


def validate_email(email):
    """Basic email validation"""
    if '@' in email and '.' in email:
        return True
    return False


def sanitize_input(text):
    """Escape HTML special characters from input"""
    return html.escape(text)
