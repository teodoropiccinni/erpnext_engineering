# All functions here are launched only once during the first installation

def setup():
    import frappe

    # Generate Roles
    def create_role(role_name, desk_access=1):
        if not frappe.db.exists("Role", role_name):
            role = frappe.get_doc({
                "doctype": "Role",
                "role_name": role_name,
                "desk_access": 1,
                "home_page": "/app/engineering"
            })
            role.insert(ignore_permissions=True)
        else:
            # Se esiste, aggiorna la Home Page
            role = frappe.get_doc("Role", role_name)
            role.home_page = "/app/engineering"
            role.save(ignore_permissions=True)

        frappe.db.commit()

    create_role("Engineering Manager")
    create_role("Engineering User")
    create_role("Engineering Viewer")

    # Generate Role Profiles
    def create_role_profile(profile_name, roles):
        if not frappe.db.exists("Role Profile", profile_name):
            frappe.get_doc({
                "doctype": "Role Profile",
                "role_profile": profile_name,
                "roles": [{"role": r} for r in roles]
            }).insert(ignore_permissions=True)

    create_role_profile("Engineering Profile", ["Engineering User", "Engineering Viewer", "Engineering Manager"])

    frappe.db.commit()
