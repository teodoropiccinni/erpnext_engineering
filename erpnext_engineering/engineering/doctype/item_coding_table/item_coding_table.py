# Copyright (c) 2025, Teodoro PICCINNI and contributors
# For license information, please see license.txt

import frappe
from frappe import logger, _
from frappe.model.document import Document

class ItemCodingTable(Document):
    def before_insert(self):
        # Set title field based on code, liv1 and liv2

        coding_code = self.engineering_item_coding_table_code or "000"
        liv1 = self.engineering_item_coding_table_liv1 or ""
        liv2 = self.engineering_item_coding_table_liv2 or ""
        code_length = self.engineering_item_coding_table_code_length or 5
        
        self.engineering_item_coding_table_title = gen_full_coding_description(coding_code, liv1, liv2, code_length)

# Check for duplicates in Item Coding Table
def is_duplicate_item_code(coding_code):
    exists = frappe.db.exists("Item", {"item_code": coding_code})
    return bool(exists)

@frappe.whitelist()
def is_duplicate_item_prefix(item_prefix):
    exists = frappe.db.exists(
        "Item Coding Table", 
        {"engineering_item_coding_table_code": item_prefix}
    )
    return bool(exists)

def validate_and_get_item_code(item_prefix, item_code):
    # Item Prefix - validate and set
    if not is_duplicate_item_prefix(item_prefix):
        item_prefix = '000'
        
    # Item Code - validate and set
    if not item_code or item_code == '00000000':
        new_item_code = generate_item_coding_code(item_prefix)
    elif is_duplicate_item_code(item_code):
        new_item_code = generate_item_coding_code(item_prefix)
        frappe.throw(_("Item code {0} already exists. New code {1} generated.").format(item_code, new_item_code))
    else:
        new_item_code = item_code
    return new_item_code

# Set DocType Item, field item_code before insert in hooks.py
@frappe.whitelist()
def set_doc_item_code(doc, method=None):
    item_code = doc.item_code
    item_prefix = doc.engineering_field_item_item_coding_table_link
    item_code = validate_and_get_item_code(item_prefix, item_code)
    doc.item_code = item_code

# Generate full coding description
@frappe.whitelist()
def gen_full_coding_description(item_coding, liv1, liv2, code_length):
    return f"{item_coding} ({liv1} - {liv2} [{code_length}])"

# Return full coding description
def get_full_coding_description(coding_code):
    item_coding = frappe.get_value("Item Coding Table", coding_code, "engineering_item_coding_table_title")
    liv1 = frappe.get_value("Item Coding Table", coding_code, "engineering_item_coding_table_liv1")
    liv2 = frappe.get_value("Item Coding Table", coding_code, "engineering_item_coding_table_liv2")
    code_length = frappe.get_value("Item Coding Table", coding_code, "engineering_item_coding_table_code_length")
    
    if not item_coding:
        frappe.throw(_("Item coding not found for code {0}").format(coding_code))
        return "Not found"
    else:
        # Concatenate vaules from Coding Table like: engineering_item_coding_table_code - engineering_item_coding_table_liv1 / engineering_item_coding_table_liv2 (engineering_item_coding_table_code_length) 
        return gen_full_coding_description(item_coding, liv1, liv2, code_length)
    
@frappe.whitelist()
def generate_item_coding_code(item_prefix='000'):
    """
    Generate a new item_code based on the provided item_prefix.
    The new code will be the first available number in the sequence from the item_code saved in DocType list Item.
    """
    # Get full code lenght based on item_coding_table_code_lenght and item_coding_table_code
    code_length = frappe.db.get_value("Item Coding Table", {"engineering_item_coding_table_code": item_prefix}, "engineering_item_coding_table_code_lenght")
    if not code_length:
        frappe.throw(_("Item Coding Table with code {0} not found.").format(item_prefix))
        logger.error(f"Item Coding Table: generate_item_coding_code - Item Coding Table with code {item_prefix} not found.")
        return None
    
    # Get the last item_code that start with the given item_prefix and calculated length
    if not item_prefix:
        frappe.throw(_("Item prefix cannot be empty."))
        logger.error("Item Coding Table: generate_item_coding_code - Item prefix cannot be empty.")
        return None

    # Get all code that 
    # - start with the given item_prefix
    item_codes_with_prefix = frappe.get_all(
        "Item",
        filters={
            "item_code": ["like", f"{item_prefix}%"]
        },
        fields=["item_code", "item_name", "engineering_field_item_item_coding_table_link"],
        order_by="item_code desc"
    )
    # - have the same code length (full_lenght = item_prefix + code_length)
    item_codes = []
    for item in item_codes_with_prefix:
        if len(item.item_code) == len(item_prefix) + int(code_length):
            item_codes.append(item)
            #stop at first match
            break
    # Get the last item_code with the given item_prefix
    last_item_code = item_codes[0].item_code if item_codes else None

    # generate new item code
    if last_item_code:
        # Increment the last item code by 1
        new_item_code = str(int(last_item_code) + 1)
    else:
        # If no last item code found, start with the item prefix
        new_item_code = item_prefix + str(0).zfill(code_length)

    return new_item_code
