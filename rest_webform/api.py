import frappe,json

@frappe.whitelist(allow_guest=True)
def post_test(**kwargs):
    kwargs=frappe._dict(kwargs) 
   
    doc = frappe.new_doc('Lead')
    #doc = frappe.new_doc('hi')
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
    phone = kwargs['telefon']
    company = kwargs['firma']
    description = kwargs['beschreibung']
    uri = kwargs['uri']
    titles=['Herr','Mr']
    if title in  titles:
        doc.salutation ='Mr'
        doc.gender = 'Male' 
    else:
        doc.salutation ='Madam'
        doc.gender = 'Female'
    doc.city = city
    doc.country = country

    doc.first_name= name
    doc.last_name = last_name
    doc.email_id = email
    doc.phone = phone 
    doc.company_name = company
    
    doc.by = kwargs
    doc_address=  frappe.new_doc('Address')
    doc_address.address_line1 = address
    doc_address.city=city 
    doc_address.country = country
    doc_address.insert(ignore_permissions=True)
    doc.insert(ignore_permissions=True)
    frappe.db.commit()
   
    return str(kwargs)