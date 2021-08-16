def swap(a, b):
    return b, a

def Permute(s, n):
    if n == 0: print(s)
    else:
        Permute(s, n-1)
        for i in range(n-1):
            s[i], s[n-1] = swap(s[i], s[n-1])
            Permute(s, n-1)
            s[i], s[n-1] = swap(s[i], s[n-1])

s=[1, 2, 3, 4]
Permute(s, 4)

