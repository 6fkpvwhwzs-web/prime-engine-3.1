import math
import time
import sys

LIMIT_N = 100_000_000

def main():
    print("=" * 65)
    print("      PRIME ENGINE 3.1 FINAL - THE ULTIMATE HYBRID")
    print("=" * 65)
    print(f"Zakres:   n = 1 do {LIMIT_N:,}")
    print(f"Max H(n): {3*LIMIT_N*(LIMIT_N+1)+1:,}")
    print("-" * 65)

    t_start = time.time()

    # KROK 1: Baza pierwszych
    max_p = math.isqrt(3 * LIMIT_N * (LIMIT_N + 1) + 1) + 1
    sys.stdout.write(f"Krok 1/3: Baza pierwszych do {max_p:,}... ")
    sys.stdout.flush()

    p_sito = bytearray(b'\x01') * max_p
    p_sito[0:2] = b'\x00\x00'
    for i in range(2, math.isqrt(max_p) + 1):
        if p_sito[i]:
            start = i * i
            p_sito[start::i] = b'\x00' * ((max_p - start - 1) // i + 1)

    t_sieve = time.time()
    print(f"gotowe ({t_sieve - t_start:.2f}s)")

    # KROK 2: Sito indeksowe
    sys.stdout.write("Krok 2/3: Sito indeksowe (pierwiastek szescienny)... ")
    sys.stdout.flush()

    sito = bytearray(b'\x01') * (LIMIT_N + 1)
    sito[0] = 0

    pos = 5
    last_update = time.time()
    total_p = 0

    while True:
        p = p_sito.find(b"\x01", pos)
        if p < 0:
            break
        pos = p + 1

        if p % 3 != 1:
            continue

        total_p += 1

        # Pierwiastek sześcienny z jedynki
        e = (p - 1) // 3
        a = 2
        w = pow(a, e, p)
        while w == 1:
            a += 1
            w = pow(a, e, p)
        
        d = (2 * w + 1) % p
        inv6 = (5 * p + 1) // 6

        roots = (
            ((d - 3) * inv6) % p,
            ((-d - 3) * inv6) % p
        )

        for r in roots:
            start = r if r > 0 else p
            if start > LIMIT_N:
                continue
            # Lokalny fix self-division
            if 3 * start * start + 3 * start + 1 == p:
                start += p
            if start <= LIMIT_N:
                count = (LIMIT_N - start) // p + 1
                sito[start::p] = b'\x00' * count

        # Ograniczenie narzutu czasu (sprawdzanie co 10k iteracji)
        if total_p % 10000 == 0 and (time.time() - last_update > 0.3):
            pct = 100 * p / max_p
            sys.stdout.write(f"\rKrok 2/3: Sito indeksowe... {pct:5.1f}% (p={p:,})   ")
            sys.stdout.flush()
            last_update = time.time()

    t_mark = time.time()
    sys.stdout.write(f"\rKrok 2/3: Sito gotowe w {t_mark - t_sieve:.2f}s   \n")
    sys.stdout.flush()

    # KROK 3: Zliczanie
    sys.stdout.write("Krok 3/3: Szybkie zliczanie... ")
    sys.stdout.flush()

    found = sito.count(1)
    
    first_5 = []
    for n in range(1, LIMIT_N + 1):
        if sito[n]:
            first_5.append((n, 3 * n * (n + 1) + 1))
        if len(first_5) == 5:
            break

    last_5 = []
    for n in range(LIMIT_N, 0, -1):
        if sito[n]:
            last_5.append((n, 3 * n * (n + 1) + 1))
        if len(last_5) == 5:
            break
    last_5.reverse()

    t_end = time.time()
    print(f"gotowe ({t_end - t_mark:.2f}s)")

    # RAPORT KOŃCOWY
    total_time = t_end - t_start
    print("\n" + "=" * 65)
    print("                 RAPORT KONCOWY")
    print("=" * 65)
    print(f"Czas bazy:      {t_sieve - t_start:.2f} s")
    print(f"Czas sita:      {t_mark - t_sieve:.2f} s")
    print(f"Czas zliczania: {t_end - t_mark:.2f} s")
    print(f"CZAS CALKOWITY: {total_time:.2f} s")
    print("-" * 65)
    print(f"ZNALEZIONE:     {found:,} liczb pierwszych")
    print(f"Gestosc:        {100 * found / LIMIT_N:.2f}%")
    print("=" * 65)

if __name__ == "__main__":
    main()
