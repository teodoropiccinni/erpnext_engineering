def setup():
    import frappe

    def create_role(role_name, desk_access=1):
        if not frappe.db.exists("Role", role_name):
            frappe.get_doc({
                "doctype": "Role",
                "role_name": role_name,
                "desk_access": desk_access
            }).insert(ignore_permissions=True)
            frappe.db.commit()

    create_role("Engineering Manager")
    create_role("Engineering User")
