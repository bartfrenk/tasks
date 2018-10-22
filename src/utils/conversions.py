def snake_to_camel(s: str) -> str:
    first, *rest = s.split('_')
    return first + ''.join(word.capitalize() for word in rest)


def snake_to_title(s: str) -> str:
    sentence = s.split('_')
    return ' '.join(word.capitalize() for word in sentence)
