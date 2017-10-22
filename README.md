# Seiken Densetsu 3 extraction tool

## Introduction

This repo is a collection of useless and incomplete tools for
Seiken Densetsu 3.

For an unknown reason, I decided to try to extract has much information from
this game as possible. This current version is only able to do few things,
mainly about text extraction.

The tools work only on the japanese version of the game. The ROM used doesn't
have a header (SHA-1: 209c55fd2a8d7963905e3048b7d40094d6bea965).

## Status

What has been done:

* Main text font extraction
* Main text decompression

What is missing:

* Automatic extraction of the main text. Even if the compression scheme is
  understood, I'm currently only able to extract the simplest dialogs.
* Graphics
* ...

## Usage

Extract the dialog 0x350 to out.png
```
./sd3.py dump_dialog rom.smc 0x350 out.png
```

Extract the font to out.png
```
./sd3.py dump_font rom.smc font.png
```

# Short list of early game dialogs

## Introduction

Dialog index | Note | Status
-------------|------|-------
0x800 | World map | KO
0xB08 | First dialog of the game | KO
0x603 | Battle ended | KO
0x220 | King | KO

## After introduction

Dialog index | Note | Status
-------------|------|-------
0x350	| Soldier | OK
0x340	| Soldier | OK
0x352	| Old man | OK
0x347	| Dog | OK
0x342	| Random guy | OK
0x7D4	| Closed door (two dialogs) | OK
0x343	| Random guy | OK
0x984	| Shop | KO
0xC0D	| Out of building transition | KO
