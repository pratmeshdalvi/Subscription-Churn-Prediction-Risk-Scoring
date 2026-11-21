import subprocess
result = subprocess.run(['pip', 'list'], capture_output=True, text=True)
for lib in ['weasyprint', 'pdfkit', 'xhtml2pdf', 'reportlab']:
    if lib in result.stdout.lower():
        print(f"Found: {lib}")
    else:
        print(f"Missing: {lib}")
