import os
import json
import re
import shutil
import logging
from .spreadsheetbench import compare_workbooks
from .docxcomp import docxml_compare
from .pptxcomp import pptxml_compare

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
logger.addHandler(console_handler)

def simple_docx_compare(result_path, answer_path, **options):
    return docxml_compare(result_path, answer_path)

def simple_pptx_compare(result_path, answer_path, **options):
    return pptxml_compare(result_path, answer_path)

# preadsheetbench original function
def compare_spreadsheet(result_path, answer_path, **options):
    """
    options need:
    - instruction_type 
    - answer_position
    """
    result, message = compare_workbooks(
        answer_path, 
        result_path,
        options['instruction_type'], 
        options['answer_position'])
    logging.info(message)
    return float(result)