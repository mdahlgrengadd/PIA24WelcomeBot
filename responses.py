from random import choice, randint

def get_response(user_input: str) -> str:
    lowered = user_input.lower()

    if lowered == '':
        return 'Well, you\'re awfully silent...'
    elif 'hello' in lowered:
        return 'Hello there!'
