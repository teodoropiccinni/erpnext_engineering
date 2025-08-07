import os
import json

import frappe
from frappe.utils import random_string
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields

def after_install():
    app_name="erpnext_engineering"
    workspace_name="Engineering"
    workspace_label="Engineering"
    workspace_title="Engineering"
    module_name = "Engineering"
    workspace_icon = "list-alt"
    workspace_indicator_color = "#3838fc"
    workspace_is_hidden = "0"
    workspace_public = True
    workspace_sequence_id = 2.2

    # Gen Module Def
    print(f"Module Def: Installing Module Def {module_name}") 
    create_engineering_module_def(module_name, app_name, workspace_icon, workspace_indicator_color)

    # Gen Workspace
    print(f"Workspace: Installing workspace {workspace_name}")
    create_engineering_workspace(workspace_title, workspace_name, module_name,  workspace_icon, workspace_indicator_color, get_engineering_workspace_content(), "", workspace_label,  workspace_public, workspace_sequence_id)

    # Adding Roles for Engineering
    print(f"Roles: Generating Roles for Module {module_name}") 
    for role in get_engineering_roles_array():
        print(f"- Role: {role}") 
        create_engineering_role(role)

    # Adding Role Profiles
    print(f"Role Profiles: Generating Roles Profiles for Module {module_name}") 
    print(f"- Engineering Manager Profile")
    create_engineering_role_profile("Engineering Manager Profile", [
        "Employee", "Engineering Manager", "Stock User", "Projects User", "Purchase User"
    ])
    print(f"- Engineering User Profile")
    create_engineering_role_profile("Engineering User Profile", [
        "Employee", "Engineering User", "Stock User", "Projects User", "Purchase User"
    ])
    print(f"- Engineering Viewer Profile")
    create_engineering_role_profile("Engineering Viewer Profile", [
        "Employee", "Engineering Viewer"
    ])

    print("Permissions: temporarly skipping adding permissions to DocTypes")
    # Adding Permissions for Engineering Manager
#    for dt in ["Item", "Item Version", "Item Coding Table", "Project", "Task"]:
#        add_engineering_role_permissions("Engineering Manager", dt, permlevel=0, perm="rwcdls")

    # Adding Permissions for Engineering User
#    for dt in ["Item", "Item Version", "Item Coding Table", "Project", "Task"]:
#        add_engineering_role_permissions("Engineering User", dt, permlevel=0, perm="rwc")

    # Adding Permissions for Engineering Viewer
#    for dt in ["Item", "Item Version", "Item Coding Table", "Project", "Task"]:
#        add_engineering_role_permissions("Engineering Viewer", dt, permlevel=0, perm="r")

def before_uninstall():
    workspace_name="Engineering"
    module_name = "Engineering"

    # TODO Implement uninstall logic to clean DB and files

    # Deleting Roles for Engineering
    for role_name in get_engineering_roles_array():
        delete_engineering_role(role_name)

    # Deleting Role Profiles for Engineering
    for role_profile in get_engineering_role_profile_array():
        delete_engineering_role_profile(role_profile)

    delete_engineering_workspace(workspace_name)

    delete_engineering_module_def(module_name)

# Workspace
"""
Create a Workspace with the given name and content blocks.

Args:
    title (str): Workspace title
    name (str): Workspace name (also used as route)
    module (str): Module to link this workspace to
    icon (str)
    indicator_color (str)
    content_blocks (list): List of dicts representing the workspace content blocks
    parent_page (str): Parent page for the workspace
    label (str): Display label (defaults to `name` if None)
    public (bool): If the workspace is visible to all users
    sequence_id (int): Sequence ID for ordering the workspace
"""
def create_engineering_workspace(
        title, 
        name,
        module, 
        icon="list-alt", 
        indicator_color="blue", 
        content_blocks=[],
        parent_page=None,
        label=None, 
        public=True,
        sequence_id=2
#        for_user = None,
#        is_hidden="0"
#        extends=None
):
    if frappe.db.exists("Workspace", name):
        print(f"Impossible to generate new Workspace: {name}. Workspace exists already")
        return
    else:
        workspace = frappe.get_doc({
            "doctype": "Workspace",
            "title": title,
            "name": name,
            "label": label or title,
            "module": module,
            "icon": icon,
            "content": content_blocks,
            "for_user": "",
            "public": public,
            "sequence_id": sequence_id,
            "parent_page": ""
        })
        workspace.insert(ignore_permissions=True)
        frappe.db.commit()
        print(f"Workspace {name} created.")

def delete_engineering_workspace(workspace_name):
    if frappe.db.exists("Workspace", workspace_name):
        frappe.delete_doc("Workspace", workspace_name, force=True)
        frappe.db.commit()
        print(f"Workspace: {workspace_name} deleted.")
    else:
        print(f"Workspace: {workspace_name} not found.")

def get_engineering_workspace_content():
    workspace_content = [
        {
            "id": "csBCiDglCE",
            "type": "header",
            "data": {
            "text": "<span class=\"h4\"><b>Le tue scorciatoie</b></span>",
            "col": 12
            }
        },
        {
            "id": "PZ7TfvN6Gq",
            "type": "shortcut",
            "data": {
            "shortcut_name": "Articoli",
            "col": 3
            }
        },
        {
            "id": "xit0dg7KvY",
            "type": "shortcut",
            "data": {
            "shortcut_name": "Elenco BOM",
            "col": 3
            }
        },
        {
            "id": "YHCQG3wAGv",
            "type": "shortcut",
            "data": {
            "shortcut_name": "BOM Creator",
            "col": 3
            }
        },
        {
            "id": "OtMcArFRa5",
            "type": "shortcut",
            "data": {
            "shortcut_name": "Progetti",
            "col": 3
            }
        },
        {
            "id": "bN_6tHS-Ct",
            "type": "spacer",
            "data": {
            "col": 12
            }
        },
        {
            "id": "yVEFZMqVwd",
            "type": "header",
            "data": {
            "text": "Funzionalità Ingegneria",
            "col": 12
            }
        },
        {
            "id": "rwrmsTI58-",
            "type": "card",
            "data": {
            "card_name": "Articoli",
            "col": 4
            }
        },
        {
            "id": "6dnsyX-siZ",
            "type": "card",
            "data": {
            "card_name": "Distinte materiali",
            "col": 4
            }
        },
        {
            "id": "CgBeLUeksT",
            "type": "card",
            "data": {
            "card_name": "Produzione",
            "col": 4
            }
        },
        {
            "id": "8OElyjEPCu",
            "type": "card",
            "data": {
            "card_name": "Progetti",
            "col": 4
            }
        },
        {
            "id": "8RRiQeYr0G",
            "type": "card",
            "data": {
            "card_name": "Tools",
            "col": 4
            }
        },
        {
            "id": "CIq-v5f5KC",
            "type": "card",
            "data": {
            "card_name": "Report",
            "col": 4
            }
        },
        {
            "id": "Pu8z7-82rT",
            "type": "card",
            "data": {
            "card_name": "Impostazioni",
            "col": 4
            }
        }
    ]

    return workspace_content

# Module Def
def create_engineering_module_def(module_name="Engineering", app_name="erpnext_engineering", icon=None, color=None):
    if frappe.db.exists("Module Def", module_name):
        print(f"Module Def: {module_name} already exists. Skipping.")
        return

    module = frappe.get_doc({
        "doctype": "Module Def",
        "module_name": module_name,
        "app_name": app_name,
        "is_custom": 0,
        "app_icon": icon or "",
        "app_color": color or ""
    })
    module.insert(ignore_permissions=True)
    frappe.db.commit()
    print(f"Module Def {module_name} created.")

def delete_engineering_module_def(module_name):
    if frappe.db.exists("Module Def", module_name):
        frappe.delete_doc("Module Def", module_name, force=True)
        frappe.db.commit()
        print(f"Module Def '{module_name}' deleted.")
    else:
        print(f"Module Def '{module_name}' not found.")


# Define Roles and other config
def get_engineering_roles_array():
    return [
        "Engineering Manager",
        "Engineering User",
        "Engineering Viewer"
    ]

def get_engineering_role_profile_array():
    return [
        "Engineering Manager Profile",
        "Engineering User Profile",
        "Engineering Viewer Profile"
    ]

#TODO: Delete role permissions


# Roles
def create_engineering_role(role_name, desk_access=1):
    if not frappe.db.exists("Role", role_name):
        role = frappe.get_doc({
            "doctype": "Role",
            "role_name": role_name,
            "desk_access": desk_access,
            "home_page": "/app/car_workshop"
        })
        role.insert(ignore_permissions=True)
    else:
        role = frappe.get_doc("Role", role_name)
        role.home_page = "/app/car_workshop"
        role.save(ignore_permissions=True)
    frappe.db.commit()

def delete_engineering_role(role_name):
    if frappe.db.exists("Role", role_name):
        frappe.delete_doc("Role", role_name, force=True)
        frappe.db.commit()
    else:
        # Role not found
        print(f"Impossible to delete Role: {role_name}. Not found")

# Role Profiles
def create_engineering_role_profile(profile_name, roles):
    if not frappe.db.exists("Role Profile", profile_name):
        frappe.get_doc({
            "doctype": "Role Profile",
            "role_profile": profile_name,
            "roles": [{"role": r} for r in roles]
        }).insert(ignore_permissions=True)
    frappe.db.commit()

def delete_engineering_role_profile(profile_name):
    if frappe.db.exists("Role Profile", profile_name):
        frappe.delete_doc("Role Profile", profile_name, force=True)
        frappe.db.commit()

# Add Role Permissions to DocType
def add_engineering_role_permissions(role, doctype, permlevel=0, perm="r"):
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

    # Evita flag non validi se il DocType non è Submittable
    if not doc.is_submittable:
        perm_flags["submit"] = False
        perm_flags["cancel"] = False

    # Verifica se il permesso già esiste
    for p in doc.permissions:
        if p.role == role and p.permlevel == permlevel:
            return  # già esiste

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
