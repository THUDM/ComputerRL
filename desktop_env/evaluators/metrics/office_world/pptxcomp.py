import zipfile
from lxml import etree
from collections import defaultdict
from .constant import (
    BODY_XMAP, LOCAL2ELEM,
    xmap_extract, meta_extract, 
    get_localname, get_table_content, get_textbox_content)

PPTXBDY = BODY_XMAP['pptx']
PPTXLOC = LOCAL2ELEM['pptx']

def pptxml_compare(init_path, answer_path):
    return get_checkpoint(init_path) == get_checkpoint(answer_path)

def get_slides(pptx_path):
    zfile = zipfile.ZipFile(pptx_path, 'r')
    zfile_list = zfile.namelist()

    body_tree = etree.fromstring(zfile.read('ppt/presentation.xml'))
    body_rel = etree.fromstring(zfile.read('ppt/_rels/presentation.xml.rels'))

    rids = meta_extract(body_rel, [".//rel:Relationship/@Id"])
    targets = meta_extract(body_rel, [".//rel:Relationship/@Target"])
    body_rel_dict = {rid: target for rid, target in zip(rids, targets)}

    slide_rids = meta_extract(body_tree, [".//p:sldIdLst/p:sldId/@r:id"])

    slide_trees = []
    slide_rels = []
    for slide_rid in slide_rids:
        slide_id = body_rel_dict[slide_rid].split('/')[-1].split('.')[0]
        slide_xml_path = f'ppt/slides/{slide_id}.xml'
        slide_rel_path = f'ppt/slides/_rels/{slide_id}.xml.rels'
        slide_trees.append(etree.fromstring(zfile.read(slide_xml_path)))
        slide_rels.append(etree.fromstring(zfile.read(slide_rel_path)))

    zfile.close()
    return slide_trees

def get_slide_info(slide_tree):
    elems = xmap_extract(slide_tree, PPTXBDY)
    elem_counter = defaultdict(int)
    content_list = []
    for elem in elems:
        name = get_localname(elem)
        elem_name = PPTXLOC[name]

        if elem_name == "textbox":
            content = get_textbox_content(elem)
            if content == "":
                continue
        elif elem_name == "table":
            content = get_table_content(elem)
        else:
            content = f"</{elem_name}>"

        content_list.append(content)
        elem_counter[elem_name] += 1

    content_list.sort()
    slide_info = {
        "content": content_list,
        "counter": elem_counter,
    }
    return slide_info

def get_checkpoint(pptx_path):
    slide_trees = get_slides(pptx_path)
    checkpoint = []
    for slide_tree in slide_trees:
        slide_info = get_slide_info(slide_tree)
        checkpoint.append(slide_info)
    return checkpoint