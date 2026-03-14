from simhash import Simhash


def compute_simhash(text: str) -> Simhash:
    return Simhash(text)


def hamming_distance(h1: Simhash, h2: Simhash) -> int:
    return h1.distance(h2)


def compute_simhash_matrix(texts: list[str]) -> list[list[int]]:
    hashes = [compute_simhash(t) for t in texts]
    n = len(hashes)
    matrix = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            dist = hamming_distance(hashes[i], hashes[j])
            matrix[i][j] = dist
            matrix[j][i] = dist
    return matrix


def find_near_duplicates(
    texts: list[str], threshold: int = 10
) -> list[dict]:
    hashes = [compute_simhash(t) for t in texts]
    duplicates = []
    for i in range(len(hashes)):
        for j in range(i + 1, len(hashes)):
            dist = hamming_distance(hashes[i], hashes[j])
            if dist <= threshold:
                duplicates.append({"i": i, "j": j, "distance": dist})
    return duplicates
