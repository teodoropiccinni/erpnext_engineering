// Copyright (c) 2025, Teodoro PICCINNI and contributors
// For license information, please see license.txt

frappe.ui.form.on("Item Coding Table", {
    validate: function(frm) {
        checkDuplicates(frm, function(is_unique) {
            if (is_unique) {
                let coding_code = frm.doc.engineering_item_coding_table_code || "000";
                let liv1 = frm.doc.engineering_item_coding_table_liv1 || "";
                let liv2 = frm.doc.engineering_item_coding_table_liv2 || "";

                let title = coding_code;
                if (liv1 && liv2) {
                    title += ` (${liv1} - ${liv2})`;
                } else if (liv1) {
                    title += ` (${liv1})`;
                }
                console.log("Code is unique, set Title: " + title);
                frm.set_value('engineering_item_coding_table_title', title);
            }
        });
    }
});

// Function to check for duplicates (with callback)
function checkDuplicates(frm, callback) {
    let coding_code = frm.doc.engineering_item_coding_table_code || "000";
    frappe.call({
        method: "erpnext_engineering.engineering.doctype.item_coding_table.item_coding_table.check_duplicates",
        args: {
            coding_code: coding_code
        },
        callback: function(response) {
            if (!response.message) {
                frappe.msgprint(__("This Item Coding Table already exists."));
                frm.set_value('engineering_item_coding_table_code', '000');
                callback(false); // Code is duplicate
            } else {
                callback(true); // No duplicates found
            }
        }
    });
}