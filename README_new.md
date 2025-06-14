[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/KjUzOSFc)

# Project 1 | Alien Love Letters – Group Info & Execution Guide

## Group Members

- Member 1: GONDA, Stephen James
- Member 2: MAGPANTAY, Antonio
- Member 3: MERCADO, Ervin Jerod
- Member 4: BUGAOAN, Carl Joseph

## Contributions

- Member 1: Part A1, A2
- Member 2: Part A1, A2, A3
- Member 3: Part B
- Member 4: Part B

## Description

This repository contains the relevant files for Project 1 of CS 21.

> > Note that the instructions loaded in Part B of the project are 16 bits long to be consistent with the format used in Part A. In example, Instructions 8 bits long can be loaded as is.

> > Instructions 16 bits long (2 separate bytes) should be concatenated first before loading.

## Part A

`A1.py` contains the assembler for Part A

`A2.py` contains the registers, the memory and the main logic for executing commands

`A2_emulator.py` contains the pyxel instance acting as the monitor for executing Arch 242 commands.

`A3.asm` contains the assembly code for running the snake program

## Part B

`B_logisim.circ` contains the Logisim-based implementation for Arch-242

## How to Run Part A1

The program runs as stated in the specifications. It takes 2 command-line arguments, where the first one would be the ilename containing Arch-242 assembly code, while the second one is bin or hex (denotes output format). It creates an output.txt which contains the assembled instructions.

example command:
python A1.py sample.asm bin

## How to Run Part A2

This part is divided into two files: `A2.py` and `A2_emulator.py`
A2_emulator.py will be the one to be used to run the asm file.

example command:
python A2_emulator.py sample.asm
