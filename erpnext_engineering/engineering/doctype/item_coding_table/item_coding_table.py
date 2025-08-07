# Copyright (c) 2025, Teodoro PICCINNI and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class ItemCodingTable(Document):
    def before_insert(self):
        coding_code = self.engineering_item_coding_table_code or "000"
        liv1 = self.engineering_item_coding_table_liv1 or ""
        liv2 = self.engineering_item_coding_table_liv2 or ""

        title = coding_code
        if liv1 and liv2:
            title += f" ({liv1} - {liv2})"
        elif liv1:
            title += f" ({liv1})"

        self.engineering_item_coding_table_title = title

# Check for duplicates in Item Coding Table
@frappe.whitelist()
def check_duplicates(coding_code):
    exists = frappe.db.exists("Item Coding Table", {"engineering_item_coding_table_code": coding_code})
    return not bool(exists)

# Return full coding description for search purposes
@frappe.whitelist()
def get_full_coding_description(coding_code):
    item_coding = frappe.get_value("Item Coding Table", coding_code, "engineering_item_coding_table_title")
    if not item_coding:
        return ""
    else:
        # Concatenate vaules from Coding Table like: engineering_item_coding_table_code - engineering_item_coding_table_liv1 / engineering_item_coding_table_liv2 (engineering_item_coding_table_code_lenght) 
        full_coding_description = f"{item_coding} - {frappe.get_value('Item Coding Table', coding_code, 'engineering_item_coding_table_liv1')} / {frappe.get_value('Item Coding Table', coding_code, 'engineering_item_coding_table_liv2')} ({frappe.get_value('Item Coding Table', coding_code, 'engineering_item_coding_table_code_lenght')})"
        return full_coding_description