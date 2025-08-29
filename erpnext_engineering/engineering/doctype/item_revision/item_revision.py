# Copyright (c) 2025, Teodoro PICCINNI and contributors
# For license information, please see license.txt

# Copyright (c) 2025, Teodoro PICCINNI and contributors
# For license information, please see license.txt

import frappe
from frappe import logger, _
from frappe.model.document import Document

class ItemRevision(Document):
    def before_insert(self):
        item_id = self.engineering_item_revision_item_id
        revision = self.engineering_item_revision_revision
        item_name = get_item_name(item_id)
        # Check and update revision
        revision = validate_and_update_revision(item_id, revision)
        # Set engineering_item_revision_revision
        self.engineering_item_revision_revision = revision
        # Set Item Code - Revision
        item_id_revision = generate_engineering_item_revision_id_revision(item_id, revision)
        self.engineering_item_revision_item_id_revision = item_id_revision
        # Set Item name
        self.engineering_item_revision_item_name = item_name

def get_last_item_revision(item_id):
    # get all revision of the selected item and order from greatest to smallest and return the engineering_item_revision_item_id of the first element
    revisions = frappe.get_all("Item Revision", filters={"engineering_item_revision_item_id": item_id}, order_by="engineering_item_revision_revision desc")
    if revisions:
        return revisions[0].engineering_item_revision_revision
    return None

# Get current item name
def get_item_name(item_id):
    item = frappe.get_doc("Item", item_id)
    if item:
        return item.item_name
    return None

# Check if engineering_item_revision_item_id_revision exists
def check_item_revision_exists(item_id, revision):
    if frappe.get_all("Item Revision", filters={"engineering_item_revision_item_id": item_id, "engineering_item_revision_revision": revision}):
        return True
    return False

def generate_new_revision_number(item_id):
    last_revision = get_last_item_revision(item_id)
    # check if last_revision is None, start from 0 else if 0 or more add 1
    if last_revision is None:
        return 0
    return last_revision + 1

def validate_and_update_revision(item_id, revision):
    # Check last revision for the selected Item
    existing_revision = get_last_item_revision(item_id)
    # If it is set, check if it already exists
    if existing_revision is not None:
        # Check if engineering_item_revision_revision is set
        if revision:
            # If revision is set and not exists in DB, check if it is last + 1
            if check_item_revision_exists(item_id, revision):
                if revision != existing_revision + 1:
                    # if it is not last +1 set it to last + 1
                    revision = existing_revision + 1
    else:
        revision = 0
    return revision

# Generate engineering_item_revision_item_id_revision from engineering_item_revision_item_id and engineering_item_revision_revision
def generate_engineering_item_revision_id_revision(engineering_item_revision_item_id, engineering_item_revision_revision):
    return f"{engineering_item_revision_item_id}-rev.{engineering_item_revision_revision}"

# Set Item revision of Form
@frappe.whitelist()
def set_doc_item_revision(doc, method=None):
    item_id = doc.engineering_item_revision_item_id
    revision = doc.engineering_item_revision_revision
    item_name = get_item_name(item_id)
    # Validate and update revision
    revision = validate_and_update_revision(item_id, revision)
    # Set doc.engineering_item_revision_revision
    doc.engineering_item_revision_revision = revision
    # Set doc.engineering_item_revision_item_id_revision as engineering_item_revision_item_id + "-" + engineering_item_revision_revision
    doc.engineering_item_revision_item_id_revision = generate_engineering_item_revision_id_revision(doc.engineering_item_revision_item_id, doc.engineering_item_revision_revision)
    # Set Item name
    doc.engineering_item_revision_item_name = item_name

