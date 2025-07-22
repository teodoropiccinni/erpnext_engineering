import frappe
import re

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
            "role_name": role_name
        }).insert(ignore_permissions=True)

    # Create User Group if it doesn't exist
    if not frappe.db.exists("User Group", group_name):
        frappe.get_doc({
            "doctype": "User Group",
            "user_group_name": group_name,
            "enabled": 1
        }).insert(ignore_permissions=True)

    # Link Role to the User Group if not already linked
    user_group = frappe.get_doc("User Group", group_name)
    if not any(r.role == role_name for r in user_group.roles):
        user_group.append("roles", {
            "role": role_name
        })
        user_group.save(ignore_permissions=True)

    # Add Role Permission for 'Item Coding Table'
    if not frappe.db.exists(
        "Custom DocPerm",
        {"parent": "Item Coding Table", "role": role_name}
    ):
        frappe.get_doc({
            "doctype": "Custom DocPerm",
            "parent": "Item Coding Table",
            "role": role_name,
            "permlevel": 0,
            "read": 1,
            "write": 1,
            "create": 1,
            "delete": 0
        }).insert(ignore_permissions=True)

    # Add Role Permission for 'Item'
    if not frappe.db.exists(
        "Custom DocPerm",
        {"parent": "Item", "role": role_name}
    ):
        frappe.get_doc({
            "doctype": "Custom DocPerm",
            "parent": "Item",
            "role": role_name,
            "permlevel": 0,
            "read": 1,
            "write": 1,
            "create": 1,
            "delete": 0
        }).insert(ignore_permissions=True)

    # Add Role Permission for 'Project'
    if not frappe.db.exists(
        "Custom DocPerm",
        {"parent": "Project", "role": role_name}
    ):
        frappe.get_doc({
            "doctype": "Custom DocPerm",
            "parent": "Project",
            "role": role_name,
            "permlevel": 0,
            "read": 1,
            "write": 1,
            "create": 1,
            "delete": 0
        }).insert(ignore_permissions=True)

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
    result = setup_workspace_access(doc.title or doc.name)
    frappe.msgprint(f"Created Group: {result['group']} | Role: {result['role']}")
