import pandas as pd
from fpdf import FPDF

# Step 1: Read data
data = pd.read_csv("data.csv")

# Step 2: Analyze data
summary = data.groupby("Department")["Salary"].agg(["count", "mean", "min", "max"]).reset_index()

# Step 3: Create PDF Report
class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 14)
        self.cell(0, 10, 'Employee Salary Report', border=False, ln=True, align='C')

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

    def chapter_title(self, title):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, title, ln=True, align='L')
        self.ln(5)

    def print_table(self, dataframe):
        self.set_font('Arial', 'B', 11)
        col_width = self.epw / len(dataframe.columns)  # evenly distribute
        for col in dataframe.columns:
            self.cell(col_width, 10, col, border=1, align='C')
        self.ln()

        self.set_font('Arial', '', 11)
        for index, row in dataframe.iterrows():
            for item in row:
                self.cell(col_width, 10, f"{item:.2f}" if isinstance(item, (int, float)) else str(item), border=1, align='C')
            self.ln()

# Step 4: Generate PDF
pdf = PDF()
pdf.add_page()
pdf.chapter_title("Department-wise Salary Summary")
pdf.print_table(summary)

# Step 5: Save
pdf.output("salary_report.pdf")

print("PDF report generated: salary_report.pdf")
