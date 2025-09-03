import frappe

patch = "20250903_migrate_item_coding_table_prefix_var"

def execute():
    print(f"Executing patch: {patch}")
    # Replace 'Item Coding Table', 'engineering_item_coding_table_code', with 'engineering_item_coding_table_prefix' with actual names
    frappe.db.sql("""
        UPDATE `tabItem Coding Table`
        SET engineering_item_coding_table_prefix = engineering_item_coding_table_code
        WHERE engineering_item_coding_table_code IS NOT NULL;
    """)
    # Now drop the old columns
    frappe.db.sql("""
        ALTER TABLE `tabItem Coding Table` 
        DROP COLUMN `engineering_item_coding_table_code_lenght`,
        DROP COLUMN `engineering_item_coding_table_naming_series`,
        DROP COLUMN `engineering_item_coding_table_code`,
        DROP INDEX `engineering_item_coding_table_code` ;
    """)