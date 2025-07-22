import frappe
from frappe.permissions import add_permission

def setup_workspace_access(workspace_name):
    """
    Create:
    - Role
    - User Group
    - Link Role to Group
    - Add Role Permissions for:
      * Item Coding Table (custom)
      * Item (standard)
      * Project (standard)
    """

    role_name = f"{workspace_name} Role"
    group_name = f"{workspace_name} Group"

    # Create Role if it doesn't exist
    if not frappe.db.exists("Role", role_name):
        frappe.get_doc({
            "doctype": "Role",
            "role_name": role_name,
        }).insert(ignore_permissions=True)

    # Create User Group if it doesn't exist
    if not frappe.db.exists("User Group", group_name):
        frappe.get_doc({
            "doctype": "User Group",
            "user_group_name": group_name,
            "enabled": 1,
            "user_group_members": []  # Required to avoid MandatoryError
        }).insert(ignore_permissions=True, ignore_mandatory=True)

    # Link Role to the User Group if not already linked
    user_group = frappe.get_doc("User Group", group_name)
    if not any(r.role == role_name for r in user_group.roles):
        user_group.append("roles", {
            "role": role_name
        })
        user_group.save(ignore_permissions=True)

    # Add Role Permissions if missing
    for doctype in ["Item Coding Table", "Item", "Project"]:
        existing_perms = frappe.get_all(
            "Custom DocPerm",
            filters={"parent": doctype, "role": role_name, "permlevel": 0},
            limit=1
        )
        if not existing_perms:
            add_permission(doctype=doctype, role=role_name, permlevel=0)

    frappe.db.commit()

    return {
        "group": group_name,
        "role": role_name
    }

@frappe.whitelist()
def create_workspace_group_and_permissions(doc, method):
    """
    Hook function for Workspace `after_insert`.
    """
    workspace_name = doc.title or doc.name
    result = setup_workspace_access(workspace_name)
    frappe.msgprint(f"Created Group: {result['group']} | Role: {result['role']}")
