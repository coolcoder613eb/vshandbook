try:
    import pyjson5 as json # Vintage story data files have trailing commas
except:
    import json

import re
import os

def html_to_typst(html):
    # Merge adjacent <hk> tags separated by +
    html = re.sub(r'</hk>\s*\+\s*<hk>', ',', html)

    # Handle <hk> tags with comma-separated keys
    def replace_hk(match):
        keys = [k.strip() for k in match.group(1).split(',')]
        return '#kbd("{}")'.format('", "'.join(keys))

    html = re.sub(r'<hk>(.*?)</hk>', replace_hk, html)

    conversions = [
        (r'<h1>(.*?)</h1>', r'=== \1'),    # <h1> to level 3
        (r'<h2>(.*?)</h2>', r'==== \1'),   # <h2> to level 4
        (r'<h3>(.*?)</h3>', r'===== \1'),  # <h3> to level 5 (added for completeness)
        (r'<strong>(.*?)</strong><br>', r'*\1* \\\n\n'),
        (r'<strong>(.*?)</strong>', r'\\\n *\1*'),
        (r'<i>(.*?)</i>', r'_\1_'),
        (r'<br>', r'\n'),
        (r'<a href="(.*?)">(.*?)</a>', r'#link("\1")[\2]'),
        (r'<font color=".*?">(.*?)</font>', r'\1'),
        (r'•\s+', r'- '),                  # Convert bullet points
        (r'\n(\d+\.\s+)', r'\n#enum[\1]'), # Numbered lists
        (r'Tip:\s*(.*)', r'#note[\1]'),    # Format tips
    ]

    for pattern, replacement in conversions:
        html = re.sub(pattern, replacement, html)

    # Clean up special characters
    html = html.replace('’', "'").replace('“', '"').replace('”', '"')
    return html

# Load the English translations from en.json
with open('en.json') as f:
    en = json.loads(f.read())

# Load guide data from the 'guides' directory
guides = []
for filename in os.listdir('guides'):
    with open(os.path.join('guides', filename)) as f:
        content = re.sub(r'(\w+):', r'"\1":', f.read())
        guides.append(json.loads(content))

# Initialize the Typst document with settings and the index
typst_guide = """#set heading(numbering: "1.")
#set par(justify: true)
#set page(
  numbering: "1",
  number-align: center,
)
#import "@preview/tablex:0.0.8": tablex, cellx
#import "@preview/note-me:0.5.0": admonition
#import "@preview/keyle:0.2.0"
#let radix_kdb(content) = box(baseline: 0.1em,
  rect(
    inset: 0.2em,
    stroke: rgb("#1c2024") + 0.3pt,
    radius: 0.25em,
    fill: rgb("#eee"),
    text(fill: black, font: (
      "Helvetica Neue",
    ), size:8pt, content),
  ),
)
#let kbd = keyle.config(theme: radix_kdb)
#let note(title: "Note", children) = admonition(
  icon-path: "icons/info.svg",
  title: title,
  color: luma(100),
  children
)
#set text(size: 15pt)

= Vintage Story Guide

#outline()

#pagebreak()

"""

# Add each guide section with a page break
for guide in guides:
    title = en[guide['title']]
    content = html_to_typst(en[guide['text']])
    typst_guide += f"""
== {title}

{content}

#pagebreak()
"""

# Write the result to guide.typ
with open('guide.typ', 'w') as f:
    f.write(typst_guide)
