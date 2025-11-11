"""
User Management System
A simple user management system with basic CRUD operations
"""

import json
import os
import tempfile

class UserManager:
    def __init__(self, filename='users.json'):
        self.filename = filename
        self.users = []
        self.load_users()

    def load_users(self):
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r', encoding='utf-8') as f:
                    self.users = json.load(f)
            except json.JSONDecodeError as e:
                print(f"Error loading users file: corrupted JSON - {e}")
                self.users = []
            except IOError as e:
                print(f"Error reading users file: {e}")
                self.users = []

    def save_users(self):
        # Atomic write: write to temp file, then replace original
        dir_name = os.path.dirname(self.filename) or '.'
        temp_fd = None
        temp_name = None
        try:
            # Create temp file in same directory
            temp_fd, temp_name = tempfile.mkstemp(dir=dir_name, prefix='.tmp_users_', suffix='.json')

            # Write JSON data to temp file
            with os.fdopen(temp_fd, 'w', encoding='utf-8') as f:
                json.dump(self.users, f)
                f.flush()
                os.fsync(f.fileno())
            temp_fd = None  # Already closed by context manager

            # Atomically replace original file
            os.replace(temp_name, self.filename)
            temp_name = None  # Successfully moved

        except (OSError, IOError) as e:
            print(f"Error saving users file: {e}")
            # Clean up temp file if it exists
            if temp_fd is not None:
                try:
                    os.close(temp_fd)
                except:
                    pass
            if temp_name is not None and os.path.exists(temp_name):
                try:
                    os.remove(temp_name)
                except:
                    pass
            raise

    def add_user(self, name, email, age):
        # TODO: Add validation
        user = {
            'id': len(self.users) + 1,
            'name': name,
            'email': email,
            'age': age
        }
        self.users.append(user)
        self.save_users()
        return user

    def get_user(self, user_id):
        for user in self.users:
            if user['id'] == user_id:
                return user
        return None

    def update_user(self, user_id, name=None, email=None, age=None):
        user = self.get_user(user_id)
        if user:
            if name is not None:
                user['name'] = name
            if email is not None:
                user['email'] = email
            if age is not None:
                user['age'] = age
            self.save_users()
            return user
        return None

    def delete_user(self, user_id):
        for i, user in enumerate(self.users):
            if user['id'] == user_id:
                del self.users[i]
                self.save_users()
                return True
        return False

    def list_users(self):
        return self.users

    def find_users_by_age(self, min_age, max_age):
        result = []
        for user in self.users:
            if user['age'] >= min_age and user['age'] <= max_age:
                result.append(user)
        return result


def main():
    manager = UserManager()

    # Add some test users
    manager.add_user('Alice', 'alice@example.com', 25)
    manager.add_user('Bob', 'bob@example.com', 30)
    manager.add_user('Charlie', 'charlie@example.com', 35)

    # List all users
    print('All users:')
    for user in manager.list_users():
        print(f"  {user['name']} ({user['email']}) - Age: {user['age']}")

    # Find users by age
    print('\nUsers aged 25-30:')
    for user in manager.find_users_by_age(25, 30):
        print(f"  {user['name']}")

    # Update a user
    manager.update_user(1, age=26)
    print(f'\nUpdated user: {manager.get_user(1)}')

    # Delete a user
    manager.delete_user(2)
    print(f'\nRemaining users: {len(manager.list_users())}')


if __name__ == '__main__':
    main()
