#!/usr/bin/env python3
import re, glob, os
from PIL import Image

HTML_GLOB = '*.html'

report = []
changed_files = []

def make_alt_from_src(src):
    name = os.path.basename(src)
    name = re.sub(r"\.[^.]+$", '', name)
    name = name.replace('-', ' ').replace('_', ' ').strip()
    return name or 'image'

for fname in glob.glob(HTML_GLOB):
    with open(fname, 'r', encoding='utf-8') as f:
        content = f.read()
    original = content
    def repl(match):
        tag = match.group(0)
        src_m = re.search(r'src\s*=\s*"([^"]+)"', tag, flags=re.I)
        if not src_m:
            return tag
        src = src_m.group(1)
        local_path = None
        if src.startswith('/'):
            local_path = os.path.join(os.getcwd(), src.lstrip('/'))
        else:
            # relative to repo root
            local_path = os.path.join(os.getcwd(), src)
        width_h = re.search(r'width\s*=\s*"([^"]*)"', tag, flags=re.I)
        height_h = re.search(r'height\s*=\s*"([^"]*)"', tag, flags=re.I)
        alt_h = re.search(r'alt\s*=\s*"([^"]*)"', tag, flags=re.I)
        loading_h = re.search(r'loading\s*=\s*"([^"]*)"', tag, flags=re.I)
        decoding_h = re.search(r'decoding\s*=\s*"([^"]*)"', tag, flags=re.I)
        new_tag = tag
        added = []
        # add loading/decoding if missing
        if not loading_h:
            # insert before closing >
            new_tag = new_tag[:-1] + ' loading="lazy"' + new_tag[-1:]
            added.append('loading')
        if not decoding_h:
            new_tag = new_tag[:-1] + ' decoding="async"' + new_tag[-1:]
            added.append('decoding')
        # alt
        if not alt_h:
            alt_text = make_alt_from_src(src)
            # insert alt
            new_tag = new_tag[:-1] + f' alt="{alt_text}"' + new_tag[-1:]
            added.append('alt')
        else:
            alt_val = alt_h.group(1).strip()
            if alt_val == '':
                alt_text = make_alt_from_src(src)
                new_tag = re.sub(r'alt\s*=\s*"[^"]*"', f'alt="{alt_text}"', new_tag, flags=re.I)
                added.append('alt-fixed')
        # dimensions
        if (not width_h or not height_h) and os.path.exists(local_path):
            try:
                with Image.open(local_path) as im:
                    w, h = im.size
                # insert width and height before last >
                if not width_h:
                    new_tag = new_tag[:-1] + f' width="{w}"' + new_tag[-1:]
                    added.append('width')
                if not height_h:
                    new_tag = new_tag[:-1] + f' height="{h}"' + new_tag[-1:]
                    added.append('height')
            except Exception as e:
                report.append((fname, 'IMG_READ_ERROR', src, str(e)))
        else:
            if (not width_h or not height_h) and not os.path.exists(local_path):
                report.append((fname, 'IMG_NOT_FOUND', src))
        if added:
            report.append((fname, 'FIXED', src, ','.join(added)))
        return new_tag

    content = re.sub(r'<img\b[^>]*>', repl, content, flags=re.I)
    if content != original:
        with open(fname, 'w', encoding='utf-8') as f:
            f.write(content)
        changed_files.append(fname)

# print summary
print('Changed files:', changed_files)
print('Report:')
for r in report:
    print(r)

# exit code 0
