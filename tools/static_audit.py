import re, glob

def scan_html_files():
    files = glob.glob('*.html')
    issues = []
    for f in files:
        with open(f, 'r', encoding='utf-8') as fh:
            lines = fh.readlines()
        for i, line in enumerate(lines, start=1):
            for tag in re.findall(r'<img\b[^>]*>', line, flags=re.I):
                attrs = tag
                has_alt = re.search(r'\balt\s*=\s*"([^"]*)"', attrs, flags=re.I)
                has_loading = re.search(r'\bloading\s*=\s*"([^"]*)"', attrs, flags=re.I)
                has_decoding = re.search(r'\bdecoding\s*=\s*"([^"]*)"', attrs, flags=re.I)
                has_width = re.search(r'\bwidth\s*=\s*"([^"]*)"', attrs, flags=re.I)
                has_height = re.search(r'\bheight\s*=\s*"([^"]*)"', attrs, flags=re.I)
                src = re.search(r'\bsrc\s*=\s*"([^"]*)"', attrs, flags=re.I)
                srcv = src.group(1) if src else ''
                if not has_alt:
                    issues.append((f, i, 'MISSING_ALT', tag.strip()))
                else:
                    altval = has_alt.group(1).strip()
                    if altval == '' or altval.lower() == '""':
                        issues.append((f, i, 'EMPTY_ALT', tag.strip()))
                if not has_loading:
                    issues.append((f, i, 'MISSING_LOADING', tag.strip()))
                if not has_decoding:
                    issues.append((f, i, 'MISSING_DECODING', tag.strip()))
                if not (has_width or has_height):
                    issues.append((f, i, 'MISSING_DIMENSIONS', tag.strip()))
        for i, line in enumerate(lines, start=1):
            if 'margin-top' in line and re.search(r'margin-top\s*:\s*\d{3,}px', line):
                issues.append((f, i, 'LARGE_INLINE_MARGIN', line.strip()))
    return files, issues

if __name__ == '__main__':
    files, issues = scan_html_files()
    print('Found HTML files:', files)
    if not issues:
        print('No issues found by static checks.')
    else:
        for it in issues:
            print(f"{it[0]}:{it[1]}: {it[2]} -> {it[3]}")
