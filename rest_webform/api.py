import frappe,json

@frappe.whitelist(allow_guest=True)
def post_test(**kwargs):
    kwargs=frappe._dict(kwargs) 
    doc = frappe.new_doc('hi')
    address= kwargs['addresse']
    titel = kwargs['titel']
    doc.by = address+titel
    doc.insert(ignore_permissions=True)
    frappe.db.commit()
   
    return str(kwargs)