import csv
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, PageBreak
from reportlab.lib.styles import getSampleStyleSheet

def create_pdf_from_csv(csv_file, pdf_file):
    with open(csv_file, 'r') as csv_file:
        data = list(csv.DictReader(csv_file))

    doc = SimpleDocTemplate(pdf_file, pagesize=letter)
    styles = getSampleStyleSheet()

    # Override 'Title' style to set left alignment
    title_style = styles['Title']
    title_style.alignment = 0  # 0 for left, 1 for center, 2 for right
    title_style.fontSize = 12

    # Story will contain the content of the PDF
    story = []

    for entry in data:
        # Add title (left-aligned)
        title = f"{entry['Title']}"
        story.append(Paragraph(title, title_style))

        # Add Presenting Author and Affiliation
        presenting_author = f"<b>Presenting Author:</b> {entry['Presenting Author']}"
        presenting_affiliation = f"{entry['Presenting Author Affiliation']}"
        presenting_author_text = f"{presenting_author}&nbsp;-&nbsp;<i><font size=8>{presenting_affiliation}</font></i>"
        story.append(Paragraph(presenting_author_text, styles['Normal']))

        # Add authors with affiliations
        authors_and_affiliations = []
        for i in range(1, 4):
            author_column = f'Author{i}'
            affiliation_column = f'Affiliation{i}'
            if entry[author_column]:
                author_text = entry[author_column]
                if entry[affiliation_column]:
                    author_text += f"&nbsp;-&nbsp;<i><font size=8>{entry[affiliation_column]}</font></i>"
                authors_and_affiliations.append(author_text)

        if authors_and_affiliations:
            authors_text = f"<b>Authors:</b><br/>- {'<br/>-&nbsp;'.join(authors_and_affiliations)}"
            story.append(Paragraph(authors_text, styles['Normal']))

        # Add blank line
        story.append(Paragraph("<br/><br/>", styles['Normal']))

        # Add description
        description_text = f"<br/> {entry['Description']}"
        story.append(Paragraph(description_text, styles['Normal']))

        # Add page break
        story.append(PageBreak())
        
    # Build the PDF document
    doc.build(story)

# Example usage
csv_file_path = 'your_data.csv'
pdf_file_path = 'output.pdf'
create_pdf_from_csv(csv_file_path, pdf_file_path)
