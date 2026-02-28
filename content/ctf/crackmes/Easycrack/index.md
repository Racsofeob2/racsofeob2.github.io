---
title: Easycrack
date: 2026-02-26
language: C/C++
platform: Windows
difficulty: 1.4/5
---

## Overview

Easycrack is a Windows x86-64 binary designed to reverse and find the password hash.

For this challenge, I will be using **IDA Free 9.2**

---

## Initial Recon

Running the binary prompts the user to enter a password

{{< figure src="images/prompt1.png" title="Program prompt requesting password" >}}

## Static Analysis

We load the binary into IDA for inspection.

In the **main** function we search for the "Password incorrect" text by pressing `Alt + T`.

{{< figure src="images/Text1.png" title="Search string" >}}

Double click the first occurrence and change from graph view to text view.

{{< figure src="images/StoredHash.png" title="Search string" >}}

Hmmm, that looks interesting lets list its cross references.

Since there is only one cross reference lets follow that.

{{< figure src="images/Hash2.png" title="Search string" >}}

Lets list cross references to it again.

{{< figure src="images/initialization.png" title="Search string" >}}

Interesting, lets investigate the reference that says "initialization".

{{< figure src="images/interesting.png" title="Search string" >}}

Great!! It looks lik it is storing a hash into a variable, lets decompile this!

```

    5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8

```

Look at that hash!! lets identify what hash algorithm is this

I'll be using [THIS SITE](https://hashes.com)

```
5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8:password:SHA256X1PLAIN
```

Amazing we have our hash broken and the password is "password" weird but it is what it is.
Lets use that when the program asks for the password.

{{< figure src="images/flag.txt.png" title="Final validation" >}}

Exellent, we found it!!

## Conclusion
Objective: Recover the password from a Windows x86-64 binary.

Approach:

- Used IDA Free 9.2 for static analysis
- Traced the "Password incorrect" string to its references
- Followed cross-references to locate the stored hash
- Identified the hash as SHA-256 and recovered the plaintext

### Key Insight

Even when not immediately obvious, following strings and cross-references systematically can uncover hardcoded secrets within a binary.
