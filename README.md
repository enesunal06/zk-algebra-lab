# zk-algebra-lab

Implementing the algebraic building blocks behind zero-knowledge proofs from scratch: finite fields, polynomials, and Lagrange interpolation.

This is not a production ZK library. It does not generate zero-knowledge proofs.

The goal is to understand the algebraic layer that many ZK systems build on before moving to full proving systems such as Groth16, PLONK, or STARKs.

## Initial scope

- finite field arithmetic over F_p
- polynomial evaluation
- polynomial addition and multiplication
- Lagrange interpolation over finite fields

## Later scope

- arithmetic circuits
- toy R1CS constraint checking

## Why this project?

Zero-knowledge proof systems rely heavily on algebraic structures such as finite fields, polynomials, and constraints.

This repository is a small from-scratch lab for understanding those building blocks through code.