// Copyright (c) 2025, Teodoro PICCINNI and contributors
// For license information, please see license.txt

frappe.ui.form.on("Item Coding Table", {
    validate: function(frm) {
        // Read variables from form
        let coding_prefix = frm.doc.engineering_item_coding_table_prefix || "000";
        let liv1 = frm.doc.engineering_item_coding_table_liv1 || "";
        let liv2 = frm.doc.engineering_item_coding_table_liv2 || "";
        let code_length = frm.doc.engineering_item_coding_table_code_length || 5;
        // Check uniqueness of prefix
        tpdev_engineering_js_item_coding_table_exists_item_prefix(coding_prefix, function(exists) {
            if (!exists) {
                console.log("Code is unique, set Title");
                return true;
            } else {
                console.log("Code is not unique, cannot set Title");
                return false;
            }
        });
        tpdev_engineering_frm_item_coding_table_set_item_title(frm, coding_prefix, liv1, liv2, code_length);
    },
    refresh: function(frm) {
        frm.trigger("validate");
    }
});

frappe.ui.form.on(
    "Item Coding Table",
    [
        "engineering_item_coding_table_prefix",
        "engineering_item_coding_table_liv1",
        "engineering_item_coding_table_liv2",
        "engineering_item_coding_table_code_length"
    ],
    function(frm) {
        console.log('Item Coding Table JS - click:engineering_item_coding_table_prefix - run:tpdev_engineering_frm_item_coding_table_gen_item_code(frm)');
        frm.trigger("validate");
    }
);

// Set title
function tpdev_engineering_frm_item_coding_table_set_item_title(frm, item_prefix, liv1, liv2, code_length) {
    frappe.call({
        method: "erpnext_engineering.engineering.doctype.item_coding_table.item_coding_table.tpdev_engineering_item_coding_table_gen_item_prefix_title",
        args: {
            item_prefix: item_prefix,
            liv1: liv1,
            liv2: liv2,
            code_length: code_length
        },
        callback: function(response) {
            if (response.message) {
                frm.set_value('engineering_item_coding_table_title', response.message);
            }
        }
    });
}

// Function to check for duplicates (with callback)
function tpdev_engineering_js_item_coding_table_exists_item_prefix(item_prefix, callback) {
    frappe.call({
        method: "erpnext_engineering.engineering.doctype.item_coding_table.item_coding_table.tpdev_engineering_item_coding_table_exists_item_prefix",
        args: {
            item_prefix: item_prefix
        },
        callback: function(response) {
            if (typeof callback === "function") {
                callback(response.message);
            }
        }
    });
}