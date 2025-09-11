frappe.ui.form.on('Item', {
//    load: function(frm) {
//        if (frm.is_new()) {
//            alert('Engineering Client Script loaded!');
//            console.log('Engineering Client Script: Item - loaded');
//        }
//    },
    refresh: function(frm) {
        toggle_item_coding_fields(frm);
        if (frm.is_new()) {
            console.log('Engineering Client Script: Item - refresh');
            if (frm.doc.engineering_field_item_enable_item_coding_prefix) {
                if (frm.doc.engineering_field_item_item_coding_table_prefix) {
                    console.log('Engineering Client Script: Item - Refresh - Proposing new Item Code');
                    tpdev_engineering_frm_item_coding_table_gen_item_code(frm);
                }
            }
        }
    },
    engineering_field_item_enable_item_coding_prefix: function(frm) {
        toggle_item_coding_fields(frm);
        if (frm.doc.engineering_field_item_enable_item_coding_prefix) {
            if (frm.doc.engineering_field_item_item_coding_table_prefix) {
                console.log('Engineering Client Script: Item - Refresh - Proposing new Item Code');
                tpdev_engineering_frm_item_coding_table_gen_item_code(frm);
            }
        }
    },
    engineering_field_item_item_coding_table_prefix: function(frm) {
        if (frm.is_new()) {
            if (frm.doc.engineering_field_item_enable_item_coding_prefix) {
                if (frm.doc.engineering_field_item_item_coding_table_prefix) {
                    console.log('Engineering Client Script: Item - Refresh - Proposing new Item Code');
                    tpdev_engineering_frm_item_coding_table_gen_item_code(frm);
                }
            }
        }
    }
});

function toggle_item_coding_fields(frm) {
    const show_prefix_list = frm.doc.engineering_field_item_enable_item_coding_prefix;
    if( show_prefix_list ) {
        enable_autocode(frm);
    } else {
        disable_autocode(frm);
    }
}

function show_item_name(frm) {
    frm.toggle_display('item_name', true); // Always show item name
}

function enable_autocode(frm) {
    frm.toggle_display('item_code', true);
    frm.set_df_property('item_code', 'read_only', 1);
    frm.set_df_property('engineering_field_item_item_coding_table_prefix', 'reqd', 1);
    frm.toggle_display('engineering_field_item_item_coding_table_prefix', true);
}

function disable_autocode(frm) {
    frm.toggle_display('item_code', true);
    frm.set_df_property('item_code', 'read_only', 0);
    frm.set_df_property('engineering_field_item_item_coding_table_prefix', 'reqd', 0);
    frm.toggle_display('engineering_field_item_item_coding_table_prefix', false);
}

function tpdev_engineering_frm_item_coding_table_gen_item_code(frm) {
    console.log('Engineering Client Script: Item - called tpdev_engineering_frm_item_coding_table_gen_item_code');
    item_coding_prefix_enable=frm.doc.engineering_field_item_enable_item_coding_prefix;
    item_coding_prefix=frm.doc.engineering_field_item_item_coding_table_prefix;
    item_code=frm.doc.item_code;
    //TODO: improve edge case management and recognition of prefixes
    if (item_coding_prefix_enable) {
        console.log('Engineering Client Script: Item - Item Code Prefix enabled');
        if (item_coding_prefix == null) {
            item_coding_prefix = '000';
            console.log(`Engineering Client Script: Item - No code prefix selected. Setting prefix to ${item_coding_prefix} from ${item_coding_prefix}`);
            frm.set_value('engineering_field_item_item_coding_table_prefix', item_coding_prefix);
        }
        console.log('Engineering Client Script: Item - API Call (tpdev_engineering_item_coding_table_gen_item_code) to generate new item code from prefix ' + item_coding_prefix);
        frappe.call({
            method: 'erpnext_engineering.engineering.doctype.item_coding_table.item_coding_table.tpdev_engineering_item_coding_table_gen_item_code',
            args: {
                'item_prefix': item_coding_prefix
            },
            timeout: 20, // 20 seconds
            callback: function(r) {
                item_code = r.message || '';
                frm.set_value('item_code', r.message || '');
            },
            error: function(xhr, status) {
                if (status === 'timeout') {
                    console.log('Engineering Client Script: Item - API Call get_item_prefix timed-out. Please try again.');
                    frappe.msgprint('Engineering Client Script: Item - API Call get_item_prefix timed-out. Please try again.');
                } else {
                    console.log('Engineering Client Script: Item - API Call get_item_prefix failed with status: ' + status);
                    frappe.msgprint('An error occurred: ' + status);
                }
            }
        });
    }
    else {
        console.log('Engineering Client Script: Item - Item Code Prefix disabled');
        if (item_code) {
            // Try to identify the code in the item coding table. If not found, set to 'null'
            console.log('Engineering Client Script: Item - API Call (tpdev_engineering_item_coding_table_get_item_prefix) to get prefix from item code ' + item_code);
            frappe.call({
                method: 'erpnext_engineering.engineering.doctype.item_coding_table.item_coding_table.tpdev_engineering_item_coding_table_get_item_prefix',
                args: {
                    'item_code': item_code
                },
                timeout: 20, // 20 seconds
                callback: function(r) {
                    console.log('Engineering Client Script: Item - API Call returned prefix: ' + (r.message || 'null'));
                    item_coding_prefix = r.message || 'null';
                    frm.set_value('engineering_field_item_item_coding_table_prefix', item_coding_prefix);
                },
                error: function(xhr, status) {
                    if (status === 'timeout') {
                        console.log('Engineering Client Script: Item - API Call get_item_prefix timed-out. Please try again.');
                        frappe.msgprint('Engineering Client Script: Item - API Call get_item_prefix timed-out. Please try again.');
                    } else {
                        console.log('Engineering Client Script: Item - API Call get_item_prefix failed with status: ' + status);
                        frappe.msgprint('An error occurred: ' + status);
                    }
                }
            });
        }
        else {
            console.log('Engineering Client Script: Item - No item code defined and Code Generation disabled.');
            frappe.msgprint('No item code defined. Cannot retrieve prefix.');
        }
    }
}