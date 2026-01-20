from extract_text import extract_only_text_from_pdf
from classes.Section import Section
from classes.Document import Document
from classes.Content import Content

raw_text = extract_only_text_from_pdf("./materials/sample.pdf")
print(raw_text)

new_doc = Document()

for page in raw_text.split("\n######################\n"):
    lines = page.split('\n')
    for i in range(len(lines)):
        if i == 0:
            section = Section(title=lines[i], level=1)
            new_doc.add_section(section)
        else:
            content_block = Content(raw_text=lines[i])
            section.add_content(content_block)

print(new_doc)