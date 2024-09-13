def fix_number(number: int, force_plus_sign=False) -> str:
    if number == 0 and not force_plus_sign:
        return '0'
    return str(number) if number < 0 else f'+{number}'
