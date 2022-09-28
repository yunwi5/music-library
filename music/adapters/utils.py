# Helper function to find out whether the name string includes the substring.
# Case insensitive search.
def search_string(name: str, substring: str):
    return substring.strip().lower() in name.lower()
