# All functions here are launched only once during the first installation
import frappe

def setup():

    # Generate Roles
    def create_role(role_name, desk_access=1):
        if not frappe.db.exists("Role", role_name):
            role = frappe.get_doc({
                "doctype": "Role",
                "role_name": role_name,
                "desk_access": desk_access,
                "home_page": "/app/engineering"
            })
            role.insert(ignore_permissions=True)
        else:
            role = frappe.get_doc("Role", role_name)
            role.home_page = "/app/engineering"
            role.save(ignore_permissions=True)
        frappe.db.commit()

    # Generate Role Profiles
    def create_role_profile(profile_name, roles):
        if not frappe.db.exists("Role Profile", profile_name):
            frappe.get_doc({
                "doctype": "Role Profile",
                "role_profile": profile_name,
                "roles": [{"role": r} for r in roles]
            }).insert(ignore_permissions=True)
        frappe.db.commit()

    # Add Role Permissions to DocType
    def add_role_permissions(role, doctype, permlevel=0, perm="r"):
        perm_flags = {
            "read": "r" in perm,
            "write": "w" in perm,
            "create": "c" in perm,
            "delete": "d" in perm,
            "submit": "s" in perm,
            "cancel": "l" in perm,
        }

        # Load the DocType definition
        doc = frappe.get_doc("DocType", doctype)

        # Check if this permission already exists
        for p in doc.permissions:
            if p.role == role and p.permlevel == permlevel:
                return  # Permission already exists, skip

        # Append new permission
        doc.append("permissions", {
            "role": role,
            "permlevel": permlevel,
            "read": perm_flags["read"],
            "write": perm_flags["write"],
            "create": perm_flags["create"],
            "delete": perm_flags["delete"],
            "submit": perm_flags["submit"],
            "cancel": perm_flags["cancel"]
        })

        doc.save()
        frappe.db.commit()

    # Adding Roles for Engineering
    create_role("Engineering Manager")
    create_role("Engineering User")
    create_role("Engineering Viewer")

    # Adding Role Profiles
    create_role_profile("Engineering Manager Profile", [
        "Employee", "Engineering Manager", "Stock User", "Projects User", "Purchase User"
    ])
    create_role_profile("Engineering User Profile", [
        "Employee", "Engineering User", "Stock User", "Projects User", "Purchase User"
    ])
    create_role_profile("Engineering Viewer Profile", [
        "Employee", "Engineering Viewer"
    ])

    # Adding Permissions for Engineering Manager
    for dt in ["Item", "Item Version", "Item Coding Table", "Project", "Task"]:
        add_role_permissions("Engineering Manager", dt, permlevel=0, perm="rwcdls")

    # Adding Permissions for Engineering User
    for dt in ["Item", "Item Version", "Item Coding Table", "Project", "Task"]:
        add_role_permissions("Engineering User", dt, permlevel=0, perm="rwc")

    # Adding Permissions for Engineering Viewer
    for dt in ["Item", "Item Version", "Item Coding Table", "Project", "Task"]:
        add_role_permissions("Engineering Viewer", dt, permlevel=0, perm="r")
