import json

def generate_summary(findings, total_files):
    """

    """
    summary = {}
    total_secrets = len(findings)
    breakdown = {}
    for item in findings:
        t = item.get("type", "Unknown")
        breakdown[t] = breakdown.get(t, 0) + 1
    summary["total_files_scanned"] = total_files
    summary["total_secrets_found"] = total_secrets
    summary["breakdown_by_type"] = breakdown
    return summary

def save_json_report(findings, total_files, output_file="leakfinder_report.json"):
    """
    Сохраняет отчет в формате JSON, включая сводную статистику.
    """
    summary = generate_summary(findings, total_files)
    report = {
        "summary": summary,
        "findings": findings
    }
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=4)
    print(f"📄 JSON отчет сохранен в {output_file}")

def save_html_report(findings, total_files, output_file="leakfinder_report.html"):
    """
    """
    summary = generate_summary(findings, total_files)
    summary_html = f"""
    <h2>Сводная статистика</h2>
    <p><strong>Отсканировано файлов:</strong> {summary["total_files_scanned"]}</p>
    <p><strong>Найдено секретов:</strong> {summary["total_secrets_found"]}</p>
    <h3>Разбивка по типам:</h3>
    <ul>
    """
    for key, count in summary["breakdown_by_type"].items():
        summary_html += f"<li><strong>{key}:</strong> {count}</li>"
    summary_html += "</ul>"

    html_content = f"""
    <html>
    <head>
        <title>LeakFinder Report</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; }}
            table {{ width: 100%; border-collapse: collapse; }}
            th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
            th {{ background-color: #f4f4f4; cursor: pointer; }}
            input[type="text"] {{
                margin-bottom: 10px;
                padding: 5px;
                width: 300px;
            }}
        </style>
    </head>
    <body>
        <h1>LeakFinder Security Report</h1>
        {summary_html}
        <h2>Найденные секреты</h2>
        <input type="text" id="searchInput" onkeyup="filterTable()" placeholder="Фильтрация по тексту...">
        <table id="reportTable">
            <thead>
                <tr>
                    <th onclick="sortTable(0)">Файл</th>
                    <th onclick="sortTable(1)">Строка</th>
                    <th onclick="sortTable(2)">Тип</th>
                    <th onclick="sortTable(3)">Найденный фрагмент</th>
                </tr>
            </thead>
            <tbody>
    """
    for finding in findings:
        html_content += f"""
            <tr>
                <td>{finding['file']}</td>
                <td>{finding['line']}</td>
                <td>{finding['type']}</td>
                <td>{finding['match']}</td>
            </tr>
        """
    html_content += """
            </tbody>
        </table>
        <script>
        // Функция сортировки таблицы
        function sortTable(n) {
            var table, rows, switching, i, x, y, shouldSwitch, dir, switchcount = 0;
            table = document.getElementById("reportTable");
            switching = true;
            dir = "asc"; 
            while (switching) {
                switching = false;
                rows = table.rows;
                for (i = 1; i < (rows.length - 1); i++) {
                    shouldSwitch = false;
                    x = rows[i].getElementsByTagName("TD")[n];
                    y = rows[i + 1].getElementsByTagName("TD")[n];
                    if (dir == "asc") {
                        if (x.innerHTML.toLowerCase() > y.innerHTML.toLowerCase()) {
                            shouldSwitch = true;
                            break;
                        }
                    } else if (dir == "desc") {
                        if (x.innerHTML.toLowerCase() < y.innerHTML.toLowerCase()) {
                            shouldSwitch = true;
                            break;
                        }
                    }
                }
                if (shouldSwitch) {
                    rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
                    switching = true;
                    switchcount++;      
                } else {
                    if (switchcount == 0 && dir == "asc") {
                        dir = "desc";
                        switching = true;
                    }
                }
            }
        }

        // Функция фильтрации таблицы
        function filterTable() {
            var input, filter, table, tr, td, i, j, txtValue;
            input = document.getElementById("searchInput");
            filter = input.value.toLowerCase();
            table = document.getElementById("reportTable");
            tr = table.getElementsByTagName("tr");
            for (i = 1; i < tr.length; i++) {
                tr[i].style.display = "none";
                td = tr[i].getElementsByTagName("td");
                for (j = 0; j < td.length; j++) {
                    if (td[j]) {
                        txtValue = td[j].textContent || td[j].innerText;
                        if (txtValue.toLowerCase().indexOf(filter) > -1) {
                            tr[i].style.display = "";
                            break;
                        }
                    }
                }
            }
        }
        </script>
    </body>
    </html>
    """
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"📄 HTML отчет сохранен в {output_file}")
