import frappe,json

@frappe.whitelist(allow_guest=True)
def post_test(**kwargs):
    doc = frappe.new_doc('hi')
    doc.hi = 'asds'
    doc.insert(ignore_permissions=True)
    frappe.db.commit()
    kwargs=frappe._dict(kwargs) 
    return str(kwargs)