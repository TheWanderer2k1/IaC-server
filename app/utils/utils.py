import random
import string
import re

class Utils:
    @staticmethod
    def generate_random_string(length: int) -> str:
        characters = string.ascii_letters + string.digits
        return ''.join(random.choice(characters) for _ in range(length))
    
    @staticmethod
    def normalize_terraform_name(name: str) -> str:
        # Convert to lowercase
        name = name.lower()
        
        # Replace spaces and dashes with underscores
        name = re.sub(r'[\s\-]+', '_', name)
        
        # Remove any characters that aren't letters, digits, or underscores
        name = re.sub(r'[^a-z0-9_]', '', name)
        
        # Ensure it starts with a letter (Terraform recommends this)
        if not name[0].isalpha():
            name = f"r_{name}"
        
        # Trim to a reasonable length (e.g., 64 characters)
        return name
    
    @staticmethod
    def remove_null_values(d):
        """
        Remove all keys with None/null values from a dictionary recursively.
        Handles nested dictionaries and lists containing dictionaries.
        """
        if isinstance(d, dict):
            # Create new dict with non-null values, recursively processing nested structures
            cleaned = {}
            for k, v in d.items():
                if v is not None:
                    cleaned_value = Utils.remove_null_values(v)
                    if cleaned_value is not None:
                        cleaned[k] = cleaned_value
            return cleaned if cleaned else None
        
        elif isinstance(d, list):
            # Process lists that might contain dictionaries
            cleaned_list = []
            for item in d:
                cleaned_item = Utils.remove_null_values(item)
                if cleaned_item is not None:
                    cleaned_list.append(cleaned_item)
            return cleaned_list if cleaned_list else None
        
        else:
            # Return the value as-is if it's not a dict or list
            return d



