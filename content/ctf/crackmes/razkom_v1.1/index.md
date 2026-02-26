---
title: Razkom_v1.1
date: 2026-02-25
language: C/C++
platform: Windows
difficulty: 1.7/5
---

## Overview

Razkom_v1.1 is a Windows x86-64 binary designed to exploit key validation by reversing the logic behind.
the objective is straightforward: analyze the program logic and build a keygen that generates valid keys.

For this challenge, I will be using **IDA Free 9.2**

---

## Initial Recon

Running the binary prompts the user to enter a valid key in order to unlock the secret flag.
{{< figure src="prompt1.png" title="Program prompt requesting key" >}}

This challenge comes with a hint about the key format.

{{< figure src="key_hint.png" title="Key format hint" >}}

**???-???-???-???-???-???** 
6 groups of 3 uppercase letters sepparated by a hyphen.

Now lets dig into the validation logic.

## Static Analysis
We will search for the string that ask to enter the key, in IDA we can do it by pressing `ALT+t`.

{{< figure src="text_search1.png" title="Searching 'Enter' string" >}}

Once we find all the ocurrences we can look for the interesting ones in the list.

{{< figure src="found1.png" title="Ocurrences list" >}}

Double click on the first one will get us to the Assembly code it references to, there we can chagne our view to graph flow by pressing `SPACE BAR`.

{{< figure src="graph1.png" title="Graph view" >}}

## Decompilation & Logic Analysis

We can switch to text view again to decompile the assembly into Pseudocode by pressing `F5` so we have a much clean structure to look at.

{{< figure src="pseudo1.png" title="Decompiled code" >}}

Good!! We can already see som checks the code performs.

```
  if ( strlen(Str) == 23
      && Str[3] == 45
      && Str[7] == 45
      && Str[11] == 45
      && Str[15] == 45
      && Str[19] == 45
      && (unsigned __int8)sub_1400010E0(Str) )
```
This conditional checks for a few things, if the input key is not 23 fails validation and gives us the **[-]Invalid key** message.
Checks if the char in positions 3,7,11,15,19 is 45 that looking into the ASCII table we know it is " - ".
We can assure that this is a basic validation that checks the minimums, length and format as we saw on the hint.
If the validtion is passed it calls function **sub_1400010E0()** giving our input as parameter

Let's dive into that function.

```c
{
  int v2; // ecx
  int v3; // r8d
  int v4; // r8d
  int v5; // r8d
  int v6; // r9d
  int v7; // r9d
  bool result; // al
  result = strlen(a1) == 23
        && (v2 = a1[2], (*a1 + a1[1]) % 26 + 65 == v2)
        && (_BYTE)v2 == 82
        && (v3 = a1[6], (a1[4] + a1[5]) % 26 + 65 == v3)
        && (_BYTE)v3 == 65
        && (v4 = a1[10], (a1[8] + a1[9]) % 26 + 65 == v4)
        && (_BYTE)v4 == 90
        && (v5 = a1[14], (a1[12] + a1[13]) % 26 + 65 == v5)
        && (_BYTE)v5 == 75
        && (v6 = a1[18], (a1[16] + a1[17]) % 26 + 65 == v6)
        && (_BYTE)v6 == 79
        && (v7 = a1[22], (a1[20] + a1[21]) % 26 + 65 == v7)
        && (_BYTE)v7 == 77;
  return result;
}
```

Excellent!! Here it is where all the magic happens lets break it down into simple terms to understand it.

After the length check it does the following

```
(v2 = a1[2], (*a1 + a1[1]) % 26 + 65 == v2) && (_BYTE)v2 == 82
```

We can see that **v2** is being assigned the value of the **a1[2]**, this means that **v2** stores the third character of the key.

### Step 1 — Remove the Noise

Lets simplify that a little bit.

```
(a1[0] + a1[1]) % 26 + 65 == a1[2] && a1[2] == 82
```

### Step 2 — Substitute the Constant

But we see at the end that the value of **a1[2]** must be 82, that number in the ASCII table corresponds to the letter "R".

```
(a1[0] + a1[1]) % 26 + 65 == 82
```

### Step 3 — Remove the ASCII Offset

Subtract 65 from both sides of the equation.

```
(a1[0] + a1[1]) % 26 = 82 - 65
```

```
(a1[0] + a1[1]) % 26 = 17
```

### Step 4 — Move to Alphabet Space

Uppercase letters are ASCII:

```
'A' = 65
...
'Z' = 90
```

So define:

```
xi = a1[i] - 65
```

This maps:

```
A → 0
B → 1
...
Z → 25
```

Now the equation becomes:

```
x0 + x1 ≡ 17 (mod 26)
```

And

```
x2 = 17  (since a1[2] = 82 → 82 - 65 = 17)
```

### What This Means

The first two characters must sum (mod 26) to 17,  
which corresponds to the letter:

```
17 → 'R'
```

So the third character is forced to be 'R', and:

```
x0 + x1 ≡ x2 (mod 26)
```

If we apply the same reasoning to the remaining blocks, we see that the third character of each group spells:

```
RAZKOM
```

And every 3-character block follows the rule:

```
(a + b) % 26 + 'A' = c
```

Which in alphabet index form becomes:

```
x(i) + x(i+1) ≡ x(i+2) (mod 26)
```

This defines the mathematical structure of the key validation.  

## Automating the Key Generation in Python

After understanding the mathematical structure of the validation logic, the next step was to automate the key construction.

We know:

- The key length is **23**
- Dashes are required at positions:
  
```
3, 7, 11, 15, 19
```

- Each 3-letter block must satisfy:

```
(a + b) % 26 + 65 = c
```

- The third letters spell:

```
RAZKOM
```

---

### Step 1 — Define the Targets

From the analysis:

```
R → 82
A → 65
Z → 90
K → 75
O → 79
M → 77
```

We store them in a list:

```python
flags = [82, 65, 90, 75, 79, 77]
```

Each value represents the required third character of each block.

---

### Step 2 — Build the Block Structure

We know there are:

```
6 blocks
3 characters per block
```

So we initialize a 2D list:

```python
g = 6
c = 3

key = [["?"] * c for _ in range(g)]
```

This creates:

```
[
  ['?', '?', '?'],
  ['?', '?', '?'],
  ...
]
```

---

### Step 3 — Apply the Modular Rule

We derived the equation:

```
x_left + x_right ≡ target (mod 26)
```

To keep it simple, we choose:

```
x_left = target
x_right = 0
```

Which guarantees:

```
target + 0 ≡ target (mod 26)
```

So the Python code becomes:

```python
for i in range(g):
    target = flags[i] - 65

    left = target
    right = 0

    key[i][0] = chr(left + 65)
    key[i][1] = chr(right + 65)
    key[i][2] = chr(flags[i])
```

Now each row contains a valid block.

---

### Step 4 — Join Blocks with Dashes

Finally, we merge everything into the final key format:

```python
final_key = "-".join("".join(row) for row in key)
print(final_key)
```

---

### Final Script

```python
def keygen(flags):
    g = 6
    c = 3

    key = [["?"] * c for _ in range(g)]

    for i in range(g):
        target = flags[i] - 65

        left = target
        right = 0

        key[i][0] = chr(left + 65)
        key[i][1] = chr(right + 65)
        key[i][2] = chr(flags[i])

    return "-".join("".join(row) for row in key)


if __name__ == "__main__":
    flags = [82, 65, 90, 75, 79, 77]
    print(keygen(flags))
```

---

### Output

```
RAR-AAA-ZAZ-KAK-OAO-MAM
```

---

### Why This Works

Each block satisfies the validation rule:

```
(a + b) % 26 + 65 = c
```

The key has the correct format and passes all validation checks.


Lets check if it will unlock the flag.

{{< figure src="flag.png" title="Secret word shown" >}}

Hooray!! we got it 


## Conclusions

Although the validation logic initially appears complex, removing compiler noise reveals a simple mathematical structure:

```
x(i) + x(i+1) ≡ x(i+2) (mod 26)
```

Each 3-character block follows modular arithmetic over the alphabet, with the third letters spelling:

```
RAZKOM
```

The key must follow a strict format (length 23 with fixed dashes), but the modular system itself is underdetermined:

```
26^6 possible valid keys
```

Ultimately, the challenge is not about brute force, but about recognizing the pattern, converting ASCII into alphabet space, and reducing the validation logic to clean modular arithmetic.
