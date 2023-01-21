import frappe,json

@frappe.whitelist(allow_guest=True)
def post_test(**kwargs):
    kwargs=frappe._dict(kwargs) 
    
    
    #doc = frappe.new_doc('hi')
    
    title = kwargs['titel']
    name= kwargs['vorname']

    last_name =  kwargs['nachname']
    address_dic= kwargs['adresse'] if kwargs['adresse'] else ''
    if address_dic:
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
    full_name = name+" "+last_name
  
    if company:
        #Customer company
        doc_customer=frappe.db.get_value('Customer',company)
    else:    
        doc_customer=frappe.db.get_value('Customer',full_name)
       
  
    if doc_customer: #Customer exists

            doc_opportunity = frappe.new_doc('Opportunity')
       
    else: #New Customer
              #Create Territory if doesn't exist
            territory = frappe.db.get_value('Territory',country)
            if territory: # territory exists 
                territory = frappe.get_doc('Territory',country)
            else: #Create territory
                territory =frappe.new_doc('Territory')
                territory.territory_name = country
                territory.insert(ignore_permissions=True)
                frappe.db.commit()
          

            #Create Address
            doc_address = frappe.new_doc('Address')
            doc_address.address_type = "Permanent"
            country_doc = frappe.db.get_value('Country',country,'name')
            if country_doc: # Country exists 
                country_doc = frappe.get_doc('Country',country)
            else: #Create Country
                country_doc =frappe.new_doc('Country')
                country_doc.country_name = country
                country_doc.insert(ignore_permissions=True)
                frappe.db.commit()
            doc_address.country = country
            doc_address.adress_line1= address
            doc_address.city = city
            doc_address.pincode = zip
            doc_address.state = state
            doc_address.title = full_name if full_name  else company
            doc_address.insert(ignore_permissions=True)
            frappe.db.commit()
            """
            #Create Contact
            doc_contact = frappe.new_doc('Contact')
            doc_contact.first_name = name
            doc_contact.last_name  = last_name 
            doc_contact.email_id = email
            doc_contact.phone = phone
            doc_contact.address =  doc_address.name
            if title in  titles:
                 doc_contact.salutation ='Mr'
                 doc_contact.gender = 'Male' 
            else:
                 doc_contact.salutation ='Madam'
                 doc_contact.gender = 'Female' 
            
            customer =frappe.new_doc('Customer')
            customer.type = "Company" if company else "Individual"
            customer.customer_name = company
            customer.customer_group ="Commercial" 
            customer.territory = country
            customer.customer_primary_address = doc_address.name
            customer.customer_primary_contact = doc_contact.name
            customer.insert(ignore_permissions=True)
            frappe.db.commit()
                """
                

   
    return str(kwargs)

def create_customer():
    pass 
def create_address():
    pass