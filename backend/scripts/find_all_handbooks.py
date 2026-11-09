import os
import re

files_to_check = []
for root, dirs, files in os.walk('.'):
    dirs[:] = [d for d in dirs if d not in {'.git', '.dart_tool', 'build', '__pycache__', 'chroma_db'}]
    for f in files:
        if f.endswith(('.dart', '.py', '.sql', '.json')):
            files_to_check.append(os.path.join(root, f))

found_titles = set()
for path in files_to_check:
    try:
        with open(path, 'r', encoding='utf-8', errors='ignore') as fp:
            content = fp.read()
            for m in re.finditer(r'title[\"\'\:\s\=]+[\"\']([^\"\']{10,120})[\"\']', content, re.IGNORECASE):
                t = m.group(1).strip()
                if any(kw in t.lower() for kw in ['cẩm nang', 'kỹ năng', 'mẹo', 'bí quyết', 'quy tắc', 'xử lý', 'thang đo', 'kinh nghiệm', 'hướng dẫn', 'quy định', 'an toàn', 'chăm sóc', 'tâm thế']):
                    found_titles.add(t)
    except Exception as e:
        pass

print(f"Total potential titles found: {len(found_titles)}")
for t in sorted(found_titles):
    print(" -", t)

