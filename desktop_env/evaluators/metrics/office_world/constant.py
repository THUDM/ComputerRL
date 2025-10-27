from lxml import etree

NAMESPACE = {
    "w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main",
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
    "rel": "http://schemas.openxmlformats.org/package/2006/relationships",
    "v": "urn:schemas-microsoft-com:vml",
    "pic": "http://schemas.openxmlformats.org/drawingml/2006/picture",
    "wp": "http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing",
    "wpc": "http://schemas.microsoft.com/office/word/2010/wordprocessingCanvas",
    "p": "http://schemas.openxmlformats.org/presentationml/2006/main",
    "s": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"
}

BODY_XMAP = {
    "docx": {
        "text": ["w:body/w:p/w:r[w:t]","w:body/w:p/w:hyperlink/w:r[w:t]"],
        "table": ["//w:tbl"],
        "image": ["//w:p/w:r/w:drawing"],
        "textbox": ["//v:textbox"],
        "footnote_ref": ["//w:p/w:r/w:footnoteReference"],
        "endnote_ref": ["//w:p/w:r/w:endnoteReference"],
        "comment_ref": ["//w:p/w:r/w:commentReference"],
        "pagebreak": ["//w:p/w:r/w:br[@w:type='page']"],
    },
    "pptx": {
        "text": ["//p:sp/p:txBody"],
        "table": ["//a:tbl"],
        "image": ["//p:pic", "//p:sp//a:blip"]
    }
}

LOCAL2ELEM = {
    "docx": {
        "r": "text",
        "tbl": "table",
        "br": "pagebreak",
        "drawing": "image",
        "textbox": "textbox",
        "footnoteReference": "footnote_ref",
        "endnoteReference": "endnote_ref",
        "commentReference": "comment_ref",
    },
    "pptx": {
        "txBody": "textbox",
        "tbl": "table",
        "pic": "image",
        "blip": "image"
    }
} 

def pure_text(texts):
    return [x.strip() for x in texts if x.strip()]

def get_localname(tree):
    return etree.QName(tree).localname

def xmap_extract(tree, xmap):
    xpath_list = []
    for v in xmap.values():
        xpath_list += v
    return meta_extract(tree, xpath_list)

def meta_extract(tree, xpath_list=[".//w:t/text()", ".//a:t/text()"]):
    tgt_xpath = '|'.join(xpath_list)
    elements = tree.xpath(
        tgt_xpath, namespaces=NAMESPACE)
    return elements

def get_table_content(tree):
    texts = []
    rows = meta_extract(tree, [".//w:tr", ".//a:tr"])
    for row in rows:
        cells = meta_extract(row, [".//w:tc", ".//a:tc"])
        row_texts = []
        for cell in cells:
            row_texts += ["".join(pure_text(meta_extract(cell)))]
        texts += [", ".join(row_texts)]
    content = "\n".join(texts)
    return content

def get_textbox_content(tree):
    raw_content = "".join(meta_extract(tree))
    content = raw_content.strip()
    return content
