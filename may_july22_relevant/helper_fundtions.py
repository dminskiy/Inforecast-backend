def generate_tag(value: str):
    # Replace forbidden chars in the name to store in the table
    tag = value.replace(' ', '_')
    return tag
