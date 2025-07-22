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