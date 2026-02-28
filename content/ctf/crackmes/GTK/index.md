---
title: GTK
date: 2026-02-24
language: C/C++
platform: Windows
difficulty: 1/5
---

## Overview

GTK is a basic Windows x86-64 binary designed as an introductory reversing challenge.  
The objective is straightforward: analyze the program logic and recover the correct password.

For this challenge, I will be using **IDA Free 9.2**.

---

## Initial Recon

Running the binary prompts the user to enter a password in order to unlock the flag.

{{< figure src="images/prompt1.png" title="Program prompt requesting password" >}}

A quick inspection confirms that this is a 64-bit Windows executable.

Since the binary is small and simple, we proceed directly to static analysis.

---

## Static Analysis

The binary is loaded into IDA for inspection.

{{< figure src="images/IDA_graph1.png" title="Control flow graph in IDA" >}}

From the control flow graph, we can observe:

- A comparison between user input and a predefined value
- A conditional jump (`jnz` – Jump if Not Zero)

The `jnz` instruction indicates that if the comparison fails, execution jumps to the failure branch. Otherwise, it proceeds toward the success path.

---

## Decompilation & Logic Analysis

To better understand the logic, we decompile the function using `F5` in IDA.

{{< figure src="images/pseudocode1.png" title="Decompiled pseudocode view" >}}

The pseudocode clearly shows the program comparing the user input against a hardcoded value.

Once we identify this value, we can simply provide it as input to satisfy the condition.

---

## Solution

After entering the correct value identified during analysis, the program reveals the flag:

{{< figure src="images/Flag.png" title="Flag output after correct input" >}}

---

## Conclusion

This challenge serves as a simple introduction to:

- Static analysis
- Control flow inspection
- Understanding conditional jumps (`jnz`)
- Basic decompilation workflow in IDA

Although straightforward, it reinforces the importance of reading program logic rather than blindly testing inputs.
