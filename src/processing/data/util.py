def sliding_window(lst: list, size: int):
    """Generate a sliding window over a list.

    :param lst: the data.
    :param size: the window size.
    :return: a generator of sliding windows.
    """
    for idx in range(len(lst) - size + 1):
        yield lst[idx: idx + size]
