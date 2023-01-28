import frappe,json



@frappe.whitelist(allow_guest=True)
def post_test(**kwargs):
    kwargs=frappe._dict(kwargs) 
    
    
    description = kwargs['beschreibung']
    url = kwargs['uri']
    owner= kwargs['owner']
    webform = kwargs['webform']
    doc_list = create_customer(kwargs)
    create_opportunity(doc_list[0], doc_list[1],description,url,owner)
      
                

   
    return str(kwargs)
@frappe.whitelist(allow_guest=True)
def create_opportunity(customer_name, contact_name,description, url,owner):
    doc_customer =frappe.get_doc('Customer',customer_name)
    doc_contact = frappe.get_doc('Contact', contact_name)
    doc_opportunity = frappe.new_doc('Opportunity')
    doc_opportunity.opportunity_from = "Customer"
    doc_opportunity.party_name = doc_customer.name
    doc_opportunity.contact_person = doc_contact.name
    doc_opportunity.opportunity_owner = owner
    doc_opportunity.description = description 
    doc_opportunity.url = url
    doc_opportunity.insert(ignore_permissions=True)
    frappe.db.commit()

def create_customer(lead):
     kwargs=frappe._dict(lead) 
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
     doc_list=[]
     titles=['Herr','Mr']
     full_name = name+" "+last_name
     if company:
        #Customer company
        customer_name=frappe.db.get_value('Customer',company,['name'])
     else:    
        customer_name=frappe.db.get_value('Customer',full_name,['name'])
     
     if customer_name: #Customer exists
        doc_customer =frappe.get_doc('Customer',customer_name)
          
        contact_name = get_contact(name,last_name,email)
        if not contact_name:
                 doc_address = create_address(country,address,city,zip,state,full_name,company)
                 doc_contact = create_contact(name,last_name, phone, doc_address,title,titles,email)
                 contact_name = get_contact(name,last_name,email)
        doc_list.append(doc_customer.name)
        doc_list.append(contact_name)
           
        return doc_list
       
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
          

            doc_address = create_address(country,address,city,zip,state,full_name,company)
            doc_contact = create_contact(name,last_name, phone, doc_address,title,titles,email)
        
          
            doc_customer =frappe.new_doc('Customer')
            doc_customer.type = "Company" if company else "Individual"
            doc_customer.customer_name = company
            doc_customer.customer_group ="Commercial" 
            doc_customer.territory = country
            doc_customer.customer_primary_address = doc_address.name
            doc_customer.customer_primary_contact = doc_contact.name
            doc_customer.insert(ignore_permissions=True)
            frappe.db.commit()
            
            doc_address.append('links',{
             'link_doctype':'Customer',
             'link_name': doc_customer.name,
            'link_title': doc_customer.name})
            doc_address.save(ignore_permissions=True)

            doc_contact.append('links',{
             'link_doctype':'Customer',
             'link_name': doc_customer.name,
            'link_title': doc_customer.name})
            doc_contact.save(ignore_permissions=True)
            frappe.db.commit()
           
            doc_list.append(doc_customer.name)
            doc_list.append(doc_contact.name)
            return doc_list

def get_contact(first_name,last_name, email):
    contact_name = frappe.db.get_value('Contact',{'first_name':first_name, 'last_name': last_name,'email_id':email},['name'])
    return contact_name
def create_address(country,address,city,zip,state,full_name,company):
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
            doc_address.address_line1= address
            doc_address.city = city
            doc_address.pincode = zip
            doc_address.state = state
            doc_address.address_title = full_name if full_name  else company
            doc_address.insert(ignore_permissions=True,ignore_mandatory=True) 
            frappe.db.commit()
            return doc_address

def create_contact(name,last_name,phone,doc_address,title,titles,email):
          #Create Contact
            doc_contact = frappe.new_doc('Contact')
            doc_contact.first_name = name
            doc_contact.last_name  = last_name 
            
            doc_contact.append('email_ids',{
             'email_id': email,
            'is_primary': 1})
            doc_contact.append('phone_nos', {
            'phone': phone,
            'is_primary_mobile_no': 1})
            doc_contact.address =  doc_address.name
            if title in  titles:
                 doc_contact.salutation ='Mister'
                 doc_contact.gender = 'Male' 
            else:
                 doc_contact.salutation ='Madam'
                 doc_contact.gender = 'Female' 
            doc_contact.insert(ignore_permissions=True,ignore_mandatory=True)
            frappe.db.commit()
            return doc_contact 
