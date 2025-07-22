import frappe
from frappe.permissions import add_permission


@frappe.whitelist()
def create_workspace_group_and_permissions(doc, method):
    """
    Hook function for Workspace `after_insert`.
    """
    workspace_name = doc.title or doc.name
#    result = setup_workspace_access(workspace_name)
    frappe.msgprint(f"Created Group: {result['group']} | Role: {result['role']}")
