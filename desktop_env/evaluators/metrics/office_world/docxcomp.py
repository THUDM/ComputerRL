import zipfile
from lxml import etree
from collections import defaultdict
from .constant import (
    BODY_XMAP, LOCAL2ELEM,
    xmap_extract, meta_extract, 
    get_localname, get_table_content, get_textbox_content)

DOCXBDY = BODY_XMAP['docx']
DOCXLOC = LOCAL2ELEM['docx']

def docxml_compare(init_path, answer_path):
    return get_checkpoint(init_path) == get_checkpoint(answer_path)

def get_notes(tree, note_type):
    content_list = []
    notes = meta_extract(tree, [f"w:{note_type}[not(@w:type)]"])
    # print(len(notes), note_type)
    for note in notes:
        tmp = list(map(lambda x: x.strip(),meta_extract(note)))
        content = "".join(tmp)
        if content:
            content_list.append(content)
    return content_list

def get_checkpoint(path):
    zfile = zipfile.ZipFile(path, 'r')
    zfile_list = zfile.namelist()
    print(zfile_list)
    tgtxml = ["document", "footnotes", "endnotes", "comments"]
    xml_dict = {
        key: etree.fromstring(zfile.read(f'word/{key}.xml')) \
        if f'word/{key}.xml' in zfile_list else None for key in tgtxml
    }
    zfile.close()

    checkpoint = defaultdict(list)

    docx_content = ""
    elems = xmap_extract(xml_dict["document"], DOCXBDY)
    for elem in elems:
        name = get_localname(elem)
        elem_name = DOCXLOC[name]
        if elem_name == "text":
            content = meta_extract(elem)
            docx_content += "".join(content)
        else:
            if elem_name == "table":
                content = get_table_content(elem)
                checkpoint[elem_name].append(content)
            elif elem_name == "textbox":
                content = get_textbox_content(elem)
                checkpoint[elem_name].append(content)
            docx_content += f"</{elem_name}>"
    checkpoint["docx_content"] = docx_content
    
    for tgt in tgtxml:
        if tgt == "document":
            continue
        if xml_dict[tgt] is None:
            checkpoint[tgt] = []
            continue
        note_type = tgt[:-1]
        checkpoint[tgt] = get_notes(xml_dict[tgt], note_type)
    return checkpoint