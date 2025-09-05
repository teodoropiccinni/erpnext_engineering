import os
import time
import json

import frappe
from frappe.utils import random_string
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields

import frappe

DEVELOPMENT_MODE_ON = frappe.conf.developer_mode
APP_NAME = "erpnext_engineering"
MODULE_NAME = "Engineering"
MODULE_PROFILE_NAME = "Engineering"
WORKSPACE_NAME = "Engineering"
WORKSPACE_LABEL = "Engineering"
WORKSPACE_TITLE = "Engineering"
WORKSPACE_ICON = "list-alt"
WORKSPACE_INDICATOR_COLOR = "#3838fc"
WORKSPACE_IS_HIDDEN = "0"
WORKSPACE_PUBLIC = True
WORKSPACE_SEQUENCE_ID = 2.2
WORKSPACE_CONTENT_FILE = "../apps/erpnext_engineering/erpnext_engineering/engineering/doctype/workspace/workspace_content.json"
WORKSPACE_LINK_FILE = "../apps/erpnext_engineering/erpnext_engineering/engineering/doctype/workspace/workspace_link.json"
CLIENT_SCRIPT_FOLDER = "../apps/erpnext_engineering/erpnext_engineering/engineering/client_script"
EMAIL_GROUP_NAME = "Engineering Team"
EMAIL_GROUP_TITLE = "Engineering Team"
EMAIL_GROUP_DESCRIPTION = "Email group for the Engineering team"

def after_engineering_app_install():
    print("Running after_install function.")
    if(DEVELOPMENT_MODE_ON):
        cwd = os.getcwd()
        print(f"Running in path: {cwd}")

    # Gen Module Def
    print(f"Module Def: Installing Module Def {MODULE_NAME}") 
    create_engineering_module_def(MODULE_NAME, APP_NAME, WORKSPACE_ICON, WORKSPACE_INDICATOR_COLOR)

    # Gen Workspace
    print(f"Workspace: Installing workspace {WORKSPACE_NAME}")
    install_engineering_workspace(WORKSPACE_TITLE, WORKSPACE_NAME, MODULE_NAME,  WORKSPACE_ICON, WORKSPACE_INDICATOR_COLOR, get_engineering_workspace_content(), get_engineering_workspace_list(), "", WORKSPACE_LABEL,  WORKSPACE_PUBLIC, WORKSPACE_SEQUENCE_ID)

    # Adding Roles for Engineering
    print(f"Roles: Generating Roles for Module {MODULE_NAME}")
    for role in get_engineering_roles_array():
        print(f"- Role: {role}") 
        create_engineering_role(role)

    # Add Module Profile
    print(f"Module Profile: Generating Module Profile for {MODULE_NAME}")
    create_engineering_module_profile(MODULE_PROFILE_NAME)

    # Adding Role Profiles
    print(f"Role Profiles: Generating Roles Profiles for Module {MODULE_NAME}") 
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
    # Enable all Client Scripts

    # Client scripts
    scripts = [
        {
            "name": "engineering_script_item_item_coding_table_prefix_check_form",
            "file": f"{CLIENT_SCRIPT_FOLDER}/engineering_script_item_item_coding_table_prefix_check.js",
            "type": "Form",
            "doctype": "Item"
        },
        {
            "name": "engineering_script_item_item_coding_table_prefix_check_list",
            "file": f"{CLIENT_SCRIPT_FOLDER}/engineering_script_item_item_coding_table_prefix_check.js",
            "type": "List",
            "doctype": "Item"
        }
    ]
    for script in scripts:
        create_or_update_client_script(script["name"], script["file"], script["type"], script["doctype"])

    # When you generate client script from here they are automatically disabled. Enabling them here
    enable_all_client_script(MODULE_NAME)
    enable_client_script("engineering_script_item_item_coding_table_prefix_check")

    # Create Email Group for Engineering
    print("Creating Email Group for Engineering")

    create_engineering_email_group(EMAIL_GROUP_NAME, EMAIL_GROUP_TITLE, EMAIL_GROUP_DESCRIPTION)

    # Custom DB constraints
    generate_item_revision_constraints()

def after_engineering_app_migrate():
    # Update Workspace
    update_engineering_workspace(WORKSPACE_NAME)
    # Custom DB constraints
    generate_item_revision_constraints()


def before_engineering_app_uninstall():
    # TODO Implement uninstall logic to clean DB and files
    # Delete Client Scripts
    delete_all_client_script(MODULE_NAME)

    # Delete Property Setters
    delete_all_property_setters(MODULE_NAME)

    # Deleting Custom Fields for Engineering
    delete_all_custom_fields(MODULE_NAME)

    # Deleting Roles for Engineering
    for role_name in get_engineering_roles_array():
        delete_engineering_role(role_name)

    # Deleting Role Profiles for Engineering
    for role_profile in get_engineering_role_profile_array():
        delete_engineering_role_profile(role_profile)

    # Deleting DocTypes for Engineering
    for doctype in frappe.get_all("DocType", filters={"module": MODULE_NAME}):
        if doctype.name not in ["Custom Field", "Role", "Role Profile"]:
            try:
                frappe.delete_doc("DocType", doctype.name, force=True)
                print(f"Deleted DocType: {doctype.name}")
            except Exception as e:
                print(f"Failed to delete DocType: {doctype.name}. Error: {e}")


    # Delete Workspace
    delete_engineering_workspace(WORKSPACE_NAME)

    # Delete Module Def
    delete_engineering_module_def(MODULE_NAME)

    # Delete Module Profile
    delete_engineering_module_profile(MODULE_PROFILE_NAME)

    # Delete Email Group
    delete_engineering_email_group(EMAIL_GROUP_NAME)

    # Delete DB constraints
    delete_engineering_item_revision_constraints()

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
def install_engineering_workspace(
        title, 
        name,
        module, 
        icon="list-alt", 
        indicator_color="blue", 
        content_blocks=[],
        link_list=[],
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
        print(type(content_blocks), content_blocks[:1])
        assert isinstance(content_blocks, list), "content_blocks must be a list"

        workspace = frappe.get_doc({
            "content": json.dumps(content_blocks),
            "docstatus": 0,
            "doctype": "Workspace",
            "for_user": "",
            "hide_custom": 0,
            "icon": icon,
            "is_hidden": 0,
            "label": label or title,
            "links": json.dumps(link_list),
            "modified": "2025-07-22 11:04:56.437006",
            "module": module,
            "name": name,
            "number_cards": [],
            "parent_page": "",
            "public": public,
            "quick_lists": [],
            "restrict_to_domain": "",
            "sequence_id": sequence_id,
            "title": title
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

def update_engineering_workspace(workspace_name):
    delete_engineering_workspace(workspace_name)
    install_engineering_workspace(WORKSPACE_TITLE, WORKSPACE_NAME, MODULE_NAME,  WORKSPACE_ICON, WORKSPACE_INDICATOR_COLOR, get_engineering_workspace_content(), get_engineering_workspace_list(), "", WORKSPACE_LABEL,  WORKSPACE_PUBLIC, WORKSPACE_SEQUENCE_ID)

#TODO currently not used, change it to read it from file
def get_engineering_workspace_content():
    # Read JSON list from file WORKSPACE_CONTENT_FILE
    with open(WORKSPACE_CONTENT_FILE, "r", encoding="utf-8") as file:
        workspace_content = json.load(file)
        assert isinstance(workspace_content, list), "get_engineering_workspace_content: Workspace content must be a list"
    return workspace_content

def get_engineering_workspace_list():
    # Read JSON list from file WORKSPACE_LINK_FILE
    with open(WORKSPACE_LINK_FILE, "r", encoding="utf-8") as file:
        workspace_link = json.load(file)
        assert isinstance(workspace_link, list), "get_engineering_workspace_list: Workspace link must be a list"
    return workspace_link



# Module Def
def create_engineering_module_def(module_name="Engineering", app_name="erpnext_engineering", icon=None, color=None):
    if frappe.db.exists("Module Def", module_name):
        print(f"Module Def: {module_name} already exists. Skipping.")
        return
    else:
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
    return

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
            "home_page": "/app/engineering"
        })
        role.insert(ignore_permissions=True)
    else:
        role = frappe.get_doc("Role", role_name)
        role.home_page = "/app/engineering"
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


# Client scripts
# Install and delete client scripts
def create_or_update_client_script(script_name, script_file, script_type, on_doctype):
    print(f"Install Client Script: {script_name}.")
    with open(script_file, 'r') as f:
        script_content = f.read()
        #convert script to one line (replace 'new line' chars with \n) and escape special chars
        script_content = script_content.replace("\"", "\\'")
    last_edit = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(os.path.getmtime(script_file)))
    # Verifica se esiste già
    if frappe.db.exists("Client Script", script_name):
        print(f"Updating Client Script: {script_name}.")
        doc = frappe.get_doc("Client Script", script_name)
        doc.docstatus = 0
        doc.doctype = "Client Script"
        doc.dt = on_doctype
        doc.enabled = 1
        doc.modified = last_edit
        doc.module = "Engineering"
        doc.name = "engineering_script_item_item_coding_table_prefix_check"
        doc.script = script_content
        doc.script_type = script_type
        doc.view = script_type
        doc.save()
    else:
        print(f"Generate new Client Script: {script_name}.")
        frappe.get_doc({
            "docstatus": 0,
            "doctype": "Client Script",
            "dt": on_doctype,
            "enabled": 1,
            "modified": last_edit,
            "module": "Engineering",
            "name": script_name,
            "script": script_content,
            "script_type": script_type,
            "view": script_type
        }).insert(ignore_permissions=True)
    frappe.db.commit()

# Enable client script by name
def enable_client_script(script_name):
    if frappe.db.exists("Client Script", script_name):
        doc = frappe.get_doc("Client Script", script_name)
        doc.enabled = 1
        doc.script_type = "Form"
        doc.save()
        print(f"Client Script: {script_name} enabled.")
    else:
        print(f"Client Script: {script_name} not found.")

# Enable all client scripts
def enable_all_client_script(module_name):
    client_scripts = frappe.get_all("Client Script", filters={"module": module_name})
    print(f"Enabling Client Scripts for module {module_name}:")
    for script in client_scripts:
        #attempt enabling Client script
        try:
            doc = frappe.get_doc("Client Script", script.name)
            doc.enabled = 1
            doc.script_type = "Form"
            doc.save()
            print(f"- {script.name}: Enabled")
        except Exception as e:
            print(f"- {script.name}: Failed to enable Client Script. Error: {e}")
        #catch and trace exception

    frappe.db.commit()
    print(f"All Client Scripts for {module_name} enabled.")
    
def delete_all_client_script(module_name):
    client_scripts = frappe.get_all("Client Script", filters={"module": module_name})
    print(f"Deleting Client Scripts for module {module_name}:")
    for script in client_scripts:
        #attempt deleting Client script
        try:
            print(f"- {script.name}: Deleted")
            frappe.delete_doc("Client Script", script.name, force=True)
        except Exception as e:
            print(f"- {script.name}: Failed to delete Client Script. Error: {e}")
        #catch and trace exception

    frappe.db.commit()
    print(f"All Client Scripts for {module_name} deleted.")

# Custom Fields
# Install and delete Custom Fields
def create_custom_fields(doctype, script_name, script):
    if frappe.db.exists("Client Script", script_name):
        print(f"Client Script: {script_name} already exists. Skipping.")
        return
    
def delete_all_custom_fields(module_name):
    custom_fields = frappe.get_all("Custom Field", filters={"module": module_name})
    print(f"Deleting Custom Fields for module {module_name}:")
    for field in custom_fields:
        #attempt deleting Custom Field
        try:
            print(f"- {field.name}: Deleted")
            frappe.delete_doc("Custom Field", field.name, force=True)
        except Exception as e:
            print(f"- {field.name}: Failed to delete Custom Field. Error: {e}")
        #catch and trace exception

    frappe.db.commit()
    print(f"All Custom Fields for {module_name} deleted.")


# Mamnage Engineering Email Groups
def create_engineering_email_group(group_name, group_title, group_description):
    if not frappe.db.exists("Email Group", group_name):
        email_group = frappe.get_doc({
            "doctype": "Email Group",
            "email_group_name": group_name,
            "title": group_title,
            "email_group_description": group_description
        })
        email_group.insert(ignore_permissions=True)
        frappe.db.commit()
        print(f"Email Group {group_name} created.")
        return email_group
    else:
        print(f"Email Group {group_name} already exists. Skipping.")
        return
def delete_engineering_email_group(group_name):
    if frappe.db.exists("Email Group", group_name):
        frappe.delete_doc("Email Group", group_name, force=True)
        frappe.db.commit()
        print(f"Email Group {group_name} deleted.")
    else:
        print(f"Email Group {group_name} not found.")
        return
    
# Property Setter
def create_property_setter(doctype, fieldname, property, value):
    if frappe.db.exists("Property Setter", f"engineering_{doctype}_{fieldname}_{property}"):
        print(f"Property Setter: engineering_{doctype}_{fieldname}_{property} already exists. Skipping.")
        return
    property_setter = frappe.get_doc({
        "doctype": "Property Setter",
        "doc_type": doctype,
        "field_name": fieldname,
        "property": property,
        "value": value
    })
    property_setter.insert(ignore_permissions=True)
    frappe.db.commit()
    print(f"Property Setter: engineering_{doctype}_{fieldname}_{property} created.")

def delete_all_property_setters(module_name):
    property_setters = frappe.get_all("Property Setter", filters={"module": module_name})
    print(f"Deleting Property Setters for module {module_name}:")
    for setter in property_setters:
        #attempt deleting Property Setter
        try:
            print(f"- {setter.name}: Deleted")
            frappe.delete_doc("Property Setter", setter.name, force=True)
        except Exception as e:
            print(f"- {setter.name}: Failed to delete Property Setter. Error: {e}")
        #catch and trace exception

    frappe.db.commit()
    print(f"All Property Setters for {module_name} deleted.")


import frappe

# Module Profile for Engineering
def create_engineering_module_profile(profile_name):
    modules = ["Project", "Manufacturing", "Stock", "Quality", "Engineering", "Purchasing"]

    # Verifica se esiste già
    if not frappe.db.exists("Module Profile", profile_name):
        doc = frappe.get_doc({
            "doctype": "Module Profile",
            "module_profile_name": profile_name,
            "module": [{"module": m} for m in modules],
            "restrict_to_domain": "",
            "custom": 1,
            "is_default": 0,
            "block_modules": 0,
            "block_standard_reports": 0,
            "block_standard_doctypes": 0
        })
        doc.insert(ignore_permissions=True)
        frappe.db.commit()
        print(f"Module Profile '{profile_name}' generated with modules: {', '.join(modules)}")
    else:
        print(f"Module Profile '{profile_name}' already exists.")

def delete_engineering_module_profile(profile_name):
    if frappe.db.exists("Module Profile", profile_name):
        frappe.delete_doc("Module Profile", profile_name, force=True)
        frappe.db.commit()
        print(f"Module Profile '{profile_name}' deleted.")
    else:
        print(f"Module Profile '{profile_name}' not found.")
# DB constraints management
def generate_item_revision_constraints():
    frappe.db.add_unique(
        "Item Revision", 
        [
            "engineering_item_revision_item_id", 
            "engineering_item_revision_revision"
        ],
        constraint_name="engineering_item_revision_unique_tuple"
    )

def delete_engineering_item_revision_constraints():
    # Remove unique constraint if exists
    constraint_name = "engineering_item_revision_unique_tuple"
    table_name = "Item Revision"
    try:
        frappe.db.sql(f'ALTER TABLE `{table_name}` DROP INDEX `{constraint_name}`')
        print(f"Removed unique constraint {constraint_name} from {table_name}")
    except Exception as e:
        print(f"Could not remove constraint {constraint_name}: {e}")