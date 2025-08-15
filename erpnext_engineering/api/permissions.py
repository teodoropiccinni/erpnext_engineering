# Copyright (c) 2015, Teodoro PICCINNI and Contributors
# License: MIT. See license.txt

import datetime

import frappe
from frappe.permissions import add_permission
from frappe import _, qb
from frappe.model.document import Document

import erpnext


def check_app_permission():
	"""Check if user has permission to access the app (for showing the app on app screen)"""
	if frappe.session.user == "Administrator":
		return True

	if frappe.has_permission("Employee", ptype="read"):
		return True

	return False

def create_workspace_group_and_permissions(doc, method):
    """
    Hook function for Workspace `after_insert`.
    """
    workspace_name = doc.title or doc.name
#    result = setup_workspace_access(workspace_name)
#    frappe.msgprint(f"Created Group: {result['group']} | Role: {result['role']}")


### TODO: from hooks.py
#  		"has_permission": "erpnext_carworkshop.api.permission.check_app_permission"
