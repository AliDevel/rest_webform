import frappe,json

@frappe.whitelist(allow_guest=True)
def post_test(**kwargs):
    kwargs=frappe._dict(kwargs) 
    doc = frappe.new_doc('hi')
    address_dic= kwargs['adresse']
    title = kwargs['titel']
    name= kwargs['vorname']
    last_name =  kwargs['nachname']
    address= address_dic['address']
    city= address_dic['city']
    zip = address_dic['postal_code']
    country = address_dic['country']
    state = address_dic['state_province']
    email= kwargs['e_mail']
    phone = kwargs['telephone']
    description = kwargs['beschreibung']
    doc.by = str(kwargs)
    doc.insert(ignore_permissions=True)
    frappe.db.commit()
   
    return str(kwargs)