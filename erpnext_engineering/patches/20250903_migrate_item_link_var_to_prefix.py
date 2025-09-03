import frappe

patch = "20250903_migrate_item_coding_table_prefix_var"

def execute():
    print(f"Executing patch: {patch}")
    # Replace 'Item Coding Table', 'engineering_item_coding_table_code', with 'engineering_item_coding_table_prefix' with actual names
    frappe.db.sql("""
        UPDATE `tabItem`
        SET engineering_field_item_item_coding_table_prefix = engineering_field_item_item_coding_table_link
        WHERE engineering_field_item_item_coding_table_link IS NOT NULL;
    """)
    # Now drop the old columns
    frappe.db.sql("""
        ALTER TABLE `tabItem` 
        DROP COLUMN `engineering_field_item_item_coding_table_link`;
    """)