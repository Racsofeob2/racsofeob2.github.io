def keygen(flags):
    g = 6
    c = 3

    # Create 6 groups of 3 letters
    key = [["?"] * c for _ in range(g)]

    for i in range(g):
        target = flags[i] - 65      

        left = 0                    
        right = target              

        key[i][0] = chr(left + 65)
        key[i][1] = chr(right + 65)
        key[i][2] = chr(flags[i])  

    return "-".join("".join(row) for row in key)


if __name__ == '__main__':
    flags = [82, 65, 90, 75, 79, 77]
    print(keygen(flags))
