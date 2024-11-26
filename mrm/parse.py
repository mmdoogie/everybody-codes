def ensure_equal_length(lines, pad_char=' '):
    longest = max(len(l) for l in lines)
    return [f'{l:{pad_char}<{longest}s}' for l in lines]
