import re

def parse_po_entries(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    entries = []
    current_entry = []
    for line in lines:
        # Entries are separated by blank lines
        if line.strip() == '' and current_entry:
            entries.append(current_entry)
            current_entry = []
        else:
            current_entry.append(line)
    # Add the last entry if not empty
    if current_entry:
        entries.append(current_entry)
    return entries

def get_first_reference(entry):
    # Find first #: line in entry and parse filename and line number
    for line in entry:
        if line.startswith('#:'):
            # Extract path and line numbers
            # example: #: .\software\templates\software\terms_conditions.html:80
            ref_line = line.strip()[2:].strip()  # remove "#:" and spaces
            # There could be multiple refs separated by spaces
            refs = ref_line.split()
            # Use the first ref
            first_ref = refs[0]
            # Separate filename and line number
            if ':' in first_ref:
                parts = first_ref.rsplit(':', 1)
                filename = parts[0]
                try:
                    lineno = int(parts[1])
                except ValueError:
                    lineno = 0
                return (filename, lineno)
            else:
                return (first_ref, 0)
    # If no reference, return something that sorts last
    return ('zzzzzzzz', 999999)

def sort_po_file(input_path, output_path):
    entries = parse_po_entries(input_path)
    # Sort by filename and line number of first reference
    entries.sort(key=lambda e: get_first_reference(e))
    with open(output_path, 'w', encoding='utf-8') as f:
        for entry in entries:
            for line in entry:
                f.write(line)
            f.write('\n')  # ensure blank line between entries

if __name__ == '__main__':
    input_po = 'locale/zh_Hans/LC_MESSAGES/django.po'  # change as needed
    output_po = 'locale/zh_Hans/LC_MESSAGES/django_sorted.po'
    sort_po_file(input_po, output_po)
    print(f"Sorted .po file saved as {output_po}")
