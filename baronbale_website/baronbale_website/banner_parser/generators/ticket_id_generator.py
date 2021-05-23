import secrets


def generate_ticket_id():
    return secrets.token_hex(10)
