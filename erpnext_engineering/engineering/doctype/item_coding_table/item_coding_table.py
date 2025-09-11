# Copyright (c) 2025, Teodoro PICCINNI and contributors
# For license information, please see license.txt

import frappe
from frappe import logger, _
from frappe.model.document import Document

class ItemCodingTable(Document):
    def before_insert(self):
        self.set_title()

    def set_title(self):
        coding_prefix = self.engineering_item_coding_table_prefix or "000"
        liv1 = self.engineering_item_coding_table_liv1 or ""
        liv2 = self.engineering_item_coding_table_liv2 or ""
        code_length = self.engineering_item_coding_table_code_length or 5
        self.engineering_item_coding_table_title = self.gen_item_prefix_title(coding_prefix, liv1, liv2, code_length)

    @staticmethod
    def exists_item_code(item_code):
        exists = frappe.db.exists("Item", {"item_code": item_code})
        return bool(exists)

    @staticmethod
    def exists_item_prefix(item_prefix):
        exists = frappe.db.exists("Item Coding Table", {"engineering_item_coding_table_prefix": item_prefix})
        return bool(exists)
    
    @staticmethod
    def gen_item_code(item_prefix):
        code_length = frappe.db.get_value("Item Coding Table", {"engineering_item_coding_table_prefix": item_prefix}, "engineering_item_coding_table_code_length")
        if not item_prefix:
            logger.error("Item Coding Table: gen_item_code - Item prefix cannot be empty.")
            frappe.throw(_("Item Coding Table: gen_item_code - Item prefix cannot be empty."))
        if not code_length:
            logger.error(f"Item Coding Table: gen_item_code - Item Coding Table with prefix {item_prefix} not found.")
            frappe.throw(_("Item Coding Table: gen_item_code - Item Coding Table with Prefix {0} not found.").format(item_prefix))
        #TODO improve selection and generation logic
        item_codes_with_prefix = frappe.get_all(
            "Item",
            filters={"item_code": ["like", f"{item_prefix}%"]},
            fields=["item_code", "item_name", "engineering_field_item_item_coding_table_prefix"],
            order_by="item_code desc"
        )
        item_codes = []
        for item in item_codes_with_prefix:
            if len(item.item_code) == len(item_prefix) + int(code_length):
                item_codes.append(item)
                break
        last_item_code = item_codes[0].item_code if item_codes else None
        if last_item_code:
            # extract numerical part of the code
            numeric_part = last_item_code[len(item_prefix):]
            new_numeric = str(int(numeric_part) + 1).zfill(code_length)
            new_item_code = item_prefix + new_numeric
        else:
            new_item_code = item_prefix + str(0).zfill(code_length)
        return new_item_code

    @staticmethod
    def gen_item_prefix_title(item_prefix, liv1, liv2, code_length):
        if not liv2:
            return f"{item_prefix} [{code_length}] ({liv1})"
        else:
            return f"{item_prefix} [{code_length}] ({liv1} - {liv2})"

    @staticmethod
    def get_item_prefix_title(item_prefix):
        # Get item_prefix, liv1, liv2, code_length, item_prefix_title Item Coding Table for the specified item_prefix
        item_prefix = frappe.get_value("Item Coding Table", item_prefix, "engineering_item_coding_table_prefix")
        if not item_prefix:
            frappe.throw(_("Item Prefix not found for Prefix {0}").format(item_prefix))
            return None
        else:
            item_prefix_title = frappe.get_value("Item Coding Table", item_prefix, "engineering_item_coding_table_title")   
            if item_prefix_title:
                return item_prefix_title
            else:
                frappe.throw(_("Item Prefix Title not set for Prefix {0}").format(item_prefix))
                return None



    @staticmethod
    def get_item_prefix(item_code):
        item_code_length = len(item_code)
        prefixes = frappe.get_all("Item Coding Table", fields=[
            "engineering_item_coding_table_prefix",
            "engineering_item_coding_table_code_length",
            "engineering_item_coding_table_code_total_length"
        ])
        matching_prefixes = []
        for prefix in prefixes:
            if prefix.engineering_item_coding_table_code_total_length == item_code_length:
                if item_code.startswith(prefix.engineering_item_coding_table_prefix):
                    matching_prefixes.append(prefix)
            elif (prefix.engineering_item_coding_table_code_length + len(prefix.engineering_item_coding_table_prefix)) == item_code_length:
                if item_code.startswith(prefix.engineering_item_coding_table_prefix):
                    matching_prefixes.append(prefix)
        if not matching_prefixes:
            frappe.throw(_("No matching item coding prefix found for item code {0}, please check the Item Coding Table and add it.").format(item_code))
            return None
        elif len(matching_prefixes) > 1:
            frappe.throw(_("Multiple matching item coding prefixes found for item code {0}, please check the Item Coding Table and remove duplicates.").format(item_code))
            return None
        else:
            item_prefix = matching_prefixes[0].engineering_item_coding_table_prefix
        return item_prefix

# --- Wrapper functions for hooks and API ---
@frappe.whitelist()
def tpdev_engineering_item_coding_table_exists_item_code(item_code):
    return ItemCodingTable.exists_item_code(item_code)

# --- Check if Item Coding Prefix already exists in Item Coding Table list ---
# Function: tpdev_engineering_item_coding_table_exists_item_prefix
# Parameters: item_prefix
# Compatible DocType: all
@frappe.whitelist()
def tpdev_engineering_item_coding_table_exists_item_prefix(item_prefix):
    return ItemCodingTable.exists_item_prefix(item_prefix)

# --- Gen Item Code in Item DocType ---
# Function: tpdev_engineering_doc_item_gen_item_code
# Parameters: doc, method
# Compatible DocType: Item
@frappe.whitelist()
def tpdev_engineering_doc_item_gen_item_code(doc, method=None):
    item_code = ItemCodingTable.gen_item_code(item_code)

# --- Set Item Prefix in Item DocType ---
# Function: tpdev_engineering_doc_item_set_item_prefix
# Parameters: doc, method
# Compatible DocType: Item
@frappe.whitelist()
def tpdev_engineering_doc_item_set_item_prefix(doc, method=None):
    item_prefix = ItemCodingTable.get_item_prefix(doc.item_code)
    doc.engineering_field_item_item_coding_table_prefix = item_prefix

@frappe.whitelist()
def tpdev_engineering_item_coding_table_gen_item_prefix_title(item_prefix, liv1, liv2, code_length):
    return ItemCodingTable.gen_item_prefix_title(item_prefix, liv1, liv2, code_length)

@frappe.whitelist()
def tpdev_engineering_item_coding_table_gen_item_code(item_prefix):
    return ItemCodingTable.gen_item_code(item_prefix)

@frappe.whitelist()
def tpdev_engineering_item_coding_table_get_item_prefix(item_code):
    return ItemCodingTable.get_item_prefix(item_code)

#----- Item hooks -----
# Before Insert - Item
@frappe.whitelist()
def tpdev_engineering_doc_item_coding_table_before_insert_item(doc, method=None):
    item_prefix_enabled = doc.engineering_field_item_enable_item_coding_prefix
    item_prefix = doc.engineering_field_item_item_coding_table_prefix
    item_code = doc.item_code
    detected_item_prefix = None
    if doc.is_new():
        # check if code engineering_field_item_enable_item_coding_prefix is enabled
        if item_prefix_enabled:
            if not item_prefix:
                if item_code:
                    detected_item_prefix = ItemCodingTable.get_item_prefix(item_code)
                    doc.engineering_field_item_item_coding_table_prefix = detected_item_prefix
                    frappe.throw(_("Item Prefix not selected. Proposing one from your item code: {0}\n").format(detected_item_prefix))
                else:
                    frappe.throw(_("Please select one Item Coding Prefix for this item."))
            elif ItemCodingTable.exists_item_prefix(item_prefix):
                item_code = ItemCodingTable.gen_item_code(item_prefix)
                doc.item_code = item_code
                frappe.msgprint(_("Item Code ({0}) generated from prefix ({1}).").format(item_code, item_prefix))
            else:
                frappe.throw(_("Item prefix {0} not found. Please select a valid Item Coding Prefix for this item.").format(item_prefix))
        else:
            if item_code:
                # check if item_code already exists
                item_code_check = ItemCodingTable.exists_item_code(item_code)
                if item_code_check:
                    # return error with indications
                    item_prefix_check = ItemCodingTable.get_item_prefix(item_code)
                    if item_prefix_check:
                        item_prefix = item_prefix_check
                        new_item_code = ItemCodingTable.gen_item_code(item_prefix)
                        frappe.throw(_("Item code {0} already exists. Proposed code: {1}. Please, copy and paste the proposed code to proceed  or enable Item Coding Prefix to auto-generate a new code.").format(item_code, new_item_code))
                    else:
                        frappe.throw(_("Item code {0} is already present in the database. Please change the code or enable Item Coding Prefix to auto-generate a new code.").format(item_code))
                else:
                    # If code is unique all good, throw error otherwise
                    if item_prefix_check:
                        frappe.msgprint(_("Item code {0} pattern recognized to Prefix: {1}. Assigning prefix.").format(item_code, item_prefix_check))
                        item_prefix = item_prefix_check
                        doc.engineering_field_item_item_coding_table_prefix = item_prefix_check
                    else:
                        frappe.msgprint(_("Item code {0} is valid but not recognized as part of any coding schema. If you know what you are doing you can ignore this message.").format(item_code))
            else:
                frappe.throw(_("Please set an Item Code or enable Item Coding Prefix to auto-generate a new code."))
    else:
        frappe.throw(_("before_insert: method called by mistake. This is not a new document"))
