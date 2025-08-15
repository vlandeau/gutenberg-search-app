def distance_with_cutoff(a: str, b: str, max_k: int) -> int | None:
    if abs(len(a) - len(b)) > max_k:
        return None
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        curr = [i]
        min_row = curr[0]
        for j, cb in enumerate(b, 1):
            cost = 0 if ca == cb else 1
            curr.append(
                min(
                    curr[-1] + 1,  # insert
                    prev[j] + 1,  # delete
                    prev[j - 1] + cost,  # substitute
                )
            )
        min_row = min(curr)
        if min_row > max_k:
            return None
        prev = curr
    return prev[-1] if prev[-1] <= max_k else None
