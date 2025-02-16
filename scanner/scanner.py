import re
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from patterns.patterns import PATTERNS

def load_ignore_list(root_directory, ignore_filename=".leakfinderignore"):
    """

    """
    ignore_paths = set()
    ignore_file = os.path.join(root_directory, ignore_filename)
    try:
        with open(ignore_file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#"):
                    ignore_paths.add(line)
    except Exception:
        # Если файла нет, игнор-лист остается пустым
        pass
    return ignore_paths

def should_ignore(file_path, ignore_list):
    """

    """
    for pattern in ignore_list:
        if pattern in file_path:
            return True
    return False

def scan_file(file_path):
    """

    """
    results = []
    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
    except Exception as e:
        print(f"Ошибка чтения файла {file_path}: {e}")
        return results


    for key, pattern in PATTERNS.items():
        for match in re.finditer(pattern, content, re.DOTALL):
            line_number = content[:match.start()].count("\n") + 1
            secret = match.group(0).strip().replace("\n", " ")
            print(f"⚠️ {key} найден в {file_path} на строке {line_number}: {secret}")
            results.append({
                "file": file_path,
                "line": line_number,
                "type": key,
                "match": secret
            })
    return results

def scan_project(directory):
    """

    """
    findings = []
    file_list = []
    ignore_list = load_ignore_list(directory)
    
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith((".py", ".js", ".go", ".json", ".yaml", ".yml", ".env", ".config", ".ini", ".txt")):
                full_path = os.path.join(root, file)
                if not should_ignore(full_path, ignore_list):
                    file_list.append(full_path)
    
    total_files = len(file_list)
    with ThreadPoolExecutor() as executor:
        future_to_file = {executor.submit(scan_file, file_path): file_path for file_path in file_list}
        for future in as_completed(future_to_file):
            result = future.result()
            findings.extend(result)
    
    return findings, total_files
