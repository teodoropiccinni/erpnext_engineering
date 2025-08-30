// Copyright (c) 2025, Teodoro PICCINNI and contributors
// For license information, please see license.txt

frappe.ui.form.on("Item Coding Table", {
    validate: function(frm) {
        // Read variables from form
        let coding_code = frm.doc.engineering_item_coding_table_code || "000";
        let liv1 = frm.doc.engineering_item_coding_table_liv1 || "";
        let liv2 = frm.doc.engineering_item_coding_table_liv2 || "";
        let code_length = frm.doc.engineering_item_coding_table_code_length || 5;
        // Check uniqueness of prefix
        is_duplicate_item_prefix(coding_code, function(is_duplicate) {
            if (!is_duplicate) {
                console.log("Code is unique, set Title");
                return true;
            } else {
                return false;
            }
        });
        set_frm_item_title(frm, coding_code, liv1, liv2, code_length);
    },
    refresh: function(frm) {
        frm.trigger("validate");
    },
    engineering_item_coding_table_code: function(frm) {
        frm.trigger("validate");
    },
    engineering_item_coding_table_liv1: function(frm) {
        frm.trigger("validate");
    },
    engineering_item_coding_table_liv2: function(frm) {
        frm.trigger("validate");
    },
    engineering_item_coding_table_code_length: function(frm) {
        frm.trigger("validate");
    }
});

frappe.ui.form.on(
    "Item Coding Table",
    'engineering_item_coding_table_code', 
    function(frm) {
        console.log('Item Coding Table JS - click:engineering_item_coding_table_code - run:generate_item_coding_code');
        frm.trigger("validate");
    }
);

// Set title
function set_frm_item_title(frm, coding_code, liv1, liv2, code_length) {
    frappe.call({
        method: "erpnext_engineering.engineering.doctype.item_coding_table.item_coding_table.gen_full_coding_description",
        args: {
            item_coding: coding_code,
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
function is_duplicate_item_prefix(item_prefix, callback) {
    frappe.call({
        method: "erpnext_engineering.engineering.doctype.item_coding_table.item_coding_table.is_duplicate_item_prefix",
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