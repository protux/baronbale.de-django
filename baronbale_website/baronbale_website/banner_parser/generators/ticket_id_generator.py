import secrets


def generate_ticket_id() -> str:
    ticket_id: str = secrets.token_hex(16)
    human_readable_ticket_id: str = (
        f"{ticket_id[0:4]}-{ticket_id[4:8]}-{ticket_id[8:12]}-{ticket_id[12:16]}"
    )
    return human_readable_ticket_id
