frappe.ui.form.on('Item', {
    load: function(frm) {
        alert('Client Script loaded!');
        console.log('Client Script: Item - loaded');
    },
    refresh: function(frm) {
        console.log('Client Script: Item - refresh');
        toggle_item_coding_fields(frm);
        generate_item_coding_code(frm);
    },
    engineering_field_item_enable_item_coding_prefix: function(frm) {
        console.log('Client Script: Item - engineering_field_item_enable_item_coding_prefix');
        toggle_item_coding_fields(frm);
        generate_item_coding_code(frm);
    },
    engineering_field_item_item_coding_table_link: function(frm) {
        console.log('Client Script: Item - engineering_field_item_item_coding_table_link');
        generate_item_coding_code(frm);
    }
});

frappe.ui.form.on('Item', 'engineering_field_item_item_coding_table_link', function(frm) {
    console.log('Client Script: Item - engineering_field_item_item_coding_table_link');
    generate_item_coding_code(frm);
});
frappe.ui.form.on('Item', 'engineering_field_item_item_coding_table_prefix', function(frm) {
    console.log('Client Script: Item - engineering_field_item_item_coding_table_prefix');
    generate_item_coding_code(frm);
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
    frm.toggle_display('engineering_field_item_item_coding_table_link', true);
}

function disable_autocode(frm) {
    frm.toggle_display('item_code', true);
    frm.set_df_property('item_code', 'read_only', 0);
    frm.toggle_display('engineering_field_item_item_coding_table_link', false);
}

function generate_item_coding_code(frm) {
    console.log('Client Script: Item - generate_item_coding_code');
    item_coding_prefix=frm.doc.engineering_field_item_item_coding_table_link;
    if (item_coding_prefix) {
        frappe.call({
            method: 'erpnext_engineering.engineering.doctype.item_coding_table.item_coding_table.generate_item_coding_code',
            args: {
                'item_prefix': item_coding_prefix
            },
            callback: function(r) {
                frm.set_value('item_code', r.message || '');
            }
        });
    } else {
        frm.set_value('item_code', '');
    }
}