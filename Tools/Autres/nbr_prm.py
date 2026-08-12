def est_premier(n):
    """Vérifie si un nombre est premier."""
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    for i in range(3, int(n**0.5) + 1, 2):
        if n % i == 0:
            return False
    return True


def main():    
    for nombre in range(1, 101):    
        if est_premier(nombre):    
            print(f"{nombre} est un nombre premier.")    


if __name__ == "__main__":
    main()
