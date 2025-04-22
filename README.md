# VS Guide to Typst Converter
Converts Vintage Story game guides from HTML to Typst format. Creates a nicely formatted document with proper headings, keyboard shortcuts and custom styling. Created to print the guides into a booklet.

## Requirements
- Python 3
- pyjson5 (optional, handles those pesky trailing commas) (otherwise you may have to remove them manually)

## Installation
```
pip install pyjson5
```

## Usage
Put your guide files in `guides/`, make sure you have `en.json` with translations, then run the script. It'll spit out `guide.typ` ready for compilation.

The script handles keyboard shortcuts, headings, formatting and uses some Typst packages (tablex, note-me, keyle) for better styling.

## Booklet
After converting, compile to PDF and create a printable booklet:
```
typst compile guide.typ
pdfbook --short-edge --paper a4paper guide.pdf
```
