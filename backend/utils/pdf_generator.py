import os
from fpdf import FPDF


def generate_invoice_pdf(invoice_id, user_name, bus_name, amount, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    file_path = os.path.join(output_dir, f"{invoice_id}.pdf")

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "BusBee Invoice", ln=True, align="C")
    pdf.ln(10)

    pdf.set_font("Arial", size=12)
    pdf.cell(0, 10, f"Invoice ID: {invoice_id}", ln=True)
    pdf.cell(0, 10, f"Customer: {user_name}", ln=True)
    pdf.cell(0, 10, f"Bus: {bus_name}", ln=True)
    pdf.cell(0, 10, f"Amount: ₹{amount}", ln=True)

    pdf.output(file_path)
    return file_path
