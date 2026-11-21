from xhtml2pdf import pisa
import os

input_html = r"C:\Users\Admin\OneDrive\Data Analyst Project\Subscription Churn Prediction & Risk Scoring\reports\Churn_Report_Print.html"
output_pdf = r"C:\Users\Admin\OneDrive\Data Analyst Project\Subscription Churn Prediction & Risk Scoring\reports\Churn_Project_Executive_Report.pdf"

with open(input_html, "r", encoding="utf-8") as f:
    html_content = f.read()

with open(output_pdf, "wb") as pdf_file:
    status = pisa.CreatePDF(html_content, dest=pdf_file)

if status.err:
    print(f"ERROR: PDF generation failed with {status.err} errors")
else:
    size_kb = os.path.getsize(output_pdf) / 1024
    print(f"PDF generated successfully: {output_pdf}")
    print(f"File size: {size_kb:.1f} KB")
