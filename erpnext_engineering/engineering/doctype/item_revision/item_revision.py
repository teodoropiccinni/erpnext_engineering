# Copyright (c) 2025, Teodoro PICCINNI and contributors
# For license information, please see license.txt

# Copyright (c) 2025, Teodoro PICCINNI and contributors
# For license information, please see license.txt

import frappe
from frappe import logger, _
from frappe.model.document import Document

class ItemRevision(Document):
    def before_insert(self):
        #check if self.engineering_item_revision_revision is empty
        if not self.engineering_item_revision_revision:
            self.engineering_item_revision_revision = 0
        # check if self.engineering_item_revision_revision exists for self.engineering_item_revision_item_id
        existing_revision = frappe.get_all("Item Revision", filters={"engineering_item_revision_item_id": self.engineering_item_revision_item_id, "engineering_item_revision_revision": self.engineering_item_revision_revision})
        if existing_revision:
            # If it exists, raise an error
            frappe.throw(_("Item Revision ID {0} already exists").format(self.engineering_item_revision_id))
        # if not exists generate a new one
        else:
            self.engineering_item_revision_id = generate_new_revision_number(self.engineering_item_revision_item_id)
        # generate generate_engineering_item_revision_id_revision
        self.engineering_item_revision_item_id_revision = generate_engineering_item_revision_id_revision(self.engineering_item_revision_item_id, self.engineering_item_revision_revision)

def get_last_item_revision(item_id):
    # get all revision of the selected item and order from greatest to smallest and return the engineering_item_revision_item_id of the first element
    revisions = frappe.get_all("Item Revision", filters={"engineering_item_revision_item_id": item_id}, order_by="creation desc")
    if revisions:
        return revisions[0].engineering_item_revision_revision
    return None

def generate_new_revision_number(item_id):
    last_revision = get_last_item_revision(item_id)
    # check if last_revision is None, start from 0 else if 0 or more add 1
    if last_revision is None:
        return 0
    return last_revision + 1

# Generate engineering_item_revision_item_id_revision from engineering_item_revision_item_id and engineering_item_revision_revision
def generate_engineering_item_revision_id_revision(engineering_item_revision_item_id, engineering_item_revision_revision):
    return f"{engineering_item_revision_item_id}-{engineering_item_revision_revision}"

# Set Item revision of Form
@frappe.whitelist()
def set_doc_item_revision(doc):
    # Check if engineering_item_revision_revision is set
    if doc.engineering_item_revision_revision:
        # If it is set, check if it already exists
        existing_revision = frappe.get_all("Item Revision", filters={"engineering_item_revision_item_id": item_id, "engineering_item_revision_revision": doc.engineering_item_revision_revision})
        if existing_revision:
            # If it is set and not exists in DB, check if it is last + 1
            last_revision = get_last_item_revision(item_id)
            if last_revision is not None and doc.engineering_item_revision_revision != last_revision + 1:
                # if it is not last +1 set it to last + 1
                doc.engineering_item_revision_revision = last_revision + 1
    # Set doc.engineering_item_revision_item_id_revision as engineering_item_revision_item_id + "-" + engineering_item_revision_revision
    doc.engineering_item_revision_item_id_revision = generate_engineering_item_revision_id_revision(doc.engineering_item_revision_item_id, doc.engineering_item_revision_revision)

