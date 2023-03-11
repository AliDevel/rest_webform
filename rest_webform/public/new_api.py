import frappe
from typing import Optional


@frappe.whitelist(allow_guest=True)
def post_api(**lead_data):
    lead_data = frappe._dict(lead_data)
    description: Optional[str] = lead_data.get('beschreibung')
    url: str = lead_data['uri']
    owner: Optional[str] = lead_data.get('owner')

    doc_customer, doc_contact = create_customer(lead_data)
    create_opportunity(lead_data, doc_customer, doc_contact, description, url, owner)

    return str(lead_data)


@frappe.whitelist(allow_guest=True)
def create_opportunity(lead_data, doc_customer, doc_contact, description, url, owner):
    doc_opportunity = frappe.new_doc('Opportunity')
    doc_opportunity.opportunity_from = "Customer"
    doc_opportunity.party_name = doc_customer.name
    doc_opportunity.contact_person = doc_contact.name
    doc_opportunity.opportunity_owner = owner
    doc_opportunity.description = '\n'.join(f'{k}: {v}' for k, v in lead_data.items() if v is not None)
    doc_opportunity.url = url
    doc_opportunity.insert(ignore_permissions=True)


def create_customer(lead_data):
    lead_data = frappe._dict(lead_data)
    title: Optional[str] = lead_data.get('titel')
    first_name: str = lead_data.get('vorname', '')
    last_name: str = lead_data.get('nachname', '')
    address_data: dict = lead_data.get('adresse', {})
    address: str = address_data.get('address', '')
    city: str = address_data.get('city', '')
    zip_code: str = address_data.get('postal_code', '')
    state: str = address_data.get('state_province', '')
    country: str = address_data.get('country', 'Germany') or 'Germany'
    email: str = lead_data.get('e_mail', '')
    phone: str = lead_data.get('telefon', '')
    company: Optional[str] = lead_data.get('firma')

    titles = ['Herr', 'Mr']
    full_name = f'{first_name} {last_name}'
    customer_name = frappe.db.get_value('Customer', company or full_name, ['name'])

    if customer_name:
        doc_customer = frappe.get_doc('Customer', customer_name)
        contact_name = get_contact(first_name, last_name, email)

        if not contact_name:
            if address:
                doc_address = create_address(country, address, city, zip_code, state, full_name, company)
            else:
                doc_address = ''
            doc_contact = create_contact(first_name, last_name, phone, doc_address, title, titles, email)
            contact_name = get_contact(first_name, last_name, email)
                                       
def get_contact(name, last_name, email):
    contact_name = frappe.db.get_value('Contact', {'first_name': name, 'last_name': last_name, 'email_id': email}, 'name')
    return contact_name


def create_contact(name, last_name, phone, doc_address, title, titles, email):
    doc_contact = frappe.new_doc('Contact')
    doc_contact.first_name = name
    doc_contact.last_name = last_name
    doc_contact.salutation = title if title in titles else ''
    doc_contact.email_id = email
    doc_contact.phone = phone
    doc_contact.address = doc_address.name
    doc_contact.insert(ignore_permissions=True)
    doc_address.append('links', {'link_doctype': 'Contact', 'link_name': doc_contact.name, 'link_title': doc_contact.name})
    doc_address.save(ignore_permissions=True)
    return doc_contact


def create_address(country, address, city, zip, state, full_name, company):
    doc_address = frappe.new_doc('Address')
    doc_address.address_title = company or full_name
    doc_address.address_line1 = address
    doc_address.city = city
    doc_address.pincode = zip
    doc_address.state = state
    doc_address.country = country
    doc_address.insert(ignore_permissions=True)
    return doc_address


def create_territory(country):
    doc_territory = frappe.new_doc('Territory')
    doc_territory.territory_name = country
    doc_territory.insert(ignore_permissions=True)
    return doc_territory.territory_name                                       