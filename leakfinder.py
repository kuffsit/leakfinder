import argparse
from scanner.scanner import scan_project
from report.report import save_json_report, save_html_report

def main():
    parser = argparse.ArgumentParser(
        description="LeakFinder - Поиск утечек API-ключей, токенов и паролей"
    )
    # Аргумент "path" не обязателен, по умолчанию сканируется текущая директория "."
    parser.add_argument(
        "path",
        nargs="?",
        default=".",
        help="Путь к проекту для анализа (по умолчанию текущая директория)"
    )
    parser.add_argument(
        "--format",
        type=str,
        choices=["json", "html"],
        default="html",
        help="Формат отчёта: json или html (по умолчанию html)"
    )
    args = parser.parse_args()

    findings, total_files = scan_project(args.path)
    if findings:
        if args.format == "json":
            save_json_report(findings, total_files)
        else:
            save_html_report(findings, total_files)
    else:
        print("✅ Утечек не найдено!")
    print("✅ Анализ завершен!")

if __name__ == "__main__":
    main()
