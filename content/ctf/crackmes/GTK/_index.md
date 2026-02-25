---
title: GTK
date: 2026-02-25
language: C/C++
platform: Windows
difficulty: 1/5
---

## Overview
GTK is a Windows x86-64 binary, very basic to Get To Know reversing engineering tools, in this case i'll be using IDA FREE 9.2

---
## Initial Recon
The file is a Windows x86-64 binary, after execution prompts for a password to unlock the flag.
{{< figure src="prompt1.png">}}

## Static Analysis
Now we are going to open the binary in IDA so we can take a look at the logic behind.
{{< figure src="IDA_graph1.png">}}
We can see that it performs some comparisons between variables
## Exploit / Solution
Lets decompile the ASSEMBLY code to pseudo code to have better understandig of what is happening.
In IDA we press F5 to decompile.
{{< figure src="pseudocode1.png">}}

good, now we can see what the program compares to our input and if we try that we will get the flag
{{< figure src="Flag.png">}}
