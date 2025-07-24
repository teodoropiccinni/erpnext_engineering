# All functions here are launched only once during the first installation
import frappe

def setup():

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
    
    # Generate Role Profiles
    def create_role_profile(profile_name, roles):
        if not frappe.db.exists("Role Profile", profile_name):
            frappe.get_doc({
                "doctype": "Role Profile",
                "role_profile": profile_name,
                "roles": [{"role": r} for r in roles]
            }).insert(ignore_permissions=True)
        frappe.db.commit()


    # Permissions assignment
    #  "read": "r"
    #  "write": "w"
    #  "create": "c"
    #  "delete": "d"
    #  "submit": "s"
    #  "cancel": "l"

    def add_role_permissions(role, doctype, permlevel=0, perm="r"):
        perm_flags = {
            "read": "r" in perm,
            "write": "w" in perm,
            "create": "c" in perm,
            "delete": "d" in perm,
            "submit": "s" in perm,
            "cancel": "l" in perm,
        }

        exists = frappe.db.exists({
            "doctype": "Role Permission for Document",
            "parent": doctype,
            "role": role,
            "permlevel": permlevel
        })

        if not exists:
            doc = frappe.get_doc({
                "doctype": "Role Permission for Document",
                "parent": doctype,
                "parentfield": "permissions",
                "parenttype": "DocType",
                "role": role,
                "permlevel": permlevel,
                "read": int(perm_flags["read"]),
                "write": int(perm_flags["write"]),
                "create": int(perm_flags["create"]),
                "delete": int(perm_flags["delete"]),
                "submit": int(perm_flags["submit"]),
                "cancel": int(perm_flags["cancel"])
            })
            doc.insert(ignore_permissions=True)
        else
            console.log("Role Permission already generated for {role} in {doctype}")

        frappe.db.commit()

    # Adding Roles for Car Workshop
    create_role("Engineering Manager")
    create_role("Engineering User")
    create_role("Engineering Viewer")

    # Adding Role Profile for Car Workshop
    create_role_profile("Engineering Profile", ["Engineering User", "Engineering Viewer", "Engineering Manager"])


    # Adding permssions for Engineering Manager
    add_role_permissions("Engineering Manager", "Item", permlevel=0, perm="rwcdls")
    add_role_permissions("Engineering Manager", "Item Version", permlevel=0, perm="rwcdls")
    add_role_permissions("Engineering Manager", "Item Coding Table", permlevel=0, perm="rwcdls")
    add_role_permissions("Engineering Manager", "Project", permlevel=0, perm="rwcdls")    
    add_role_permissions("Engineering Manager", "Task", permlevel=0, perm="rwcdls")       

    # Adding permissions for Engineering User
    add_role_permissions("Engineering User", "Item", permlevel=0, perm="rwc")
    add_role_permissions("Engineering User", "Item Version", permlevel=0, perm="rwc")  
    add_role_permissions("Engineering User", "Item Coding Table", permlevel=0, perm="rwc")
    add_role_permissions("Engineering User", "Project", permlevel=0, perm="rwc")
    add_role_permissions("Engineering User", "Task", permlevel=0, perm="rwc")

    # Adding permissions for Engineering Viewer
    add_role_permissions("Engineering Viewer", "Item", permlevel=0, perm="r")
    add_role_permissions("Engineering Viewer", "Item Version", permlevel=0, perm="r")
    add_role_permissions("Engineering Viewer", "Item Coding Table", permlevel=0, perm="r")
    add_role_permissions("Engineering Viewer", "Project", permlevel=0, perm="r")
    add_role_permissions("Engineering Viewer", "Task", permlevel=0, perm="r")
