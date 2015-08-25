"""
bbofuser: apps.v1api
FILE: practitioner
Created: 8/21/15 10:14 AM

functions for managing Practitioner Profile

"""
__author__ = 'Mark Scrimshire:@ekivemark'

from datetime import datetime
from django.conf import settings

from apps.v1api.utils import date_to_iso
from apps.v1api.views.fhir_elements import (npid,
                                            human_name,
                                            contact_point,
                                            address,
                                            )


def write_practitioner_narrative(profile):
    """
    Write a Practitioner Narrative section using the Practitioner Profile
    :param profile:
    :return: text string
    """
    # Use <br/> to force line breaks. <br> will not validate successfully

    narrative = "Welcome to my Practice..."

    narrative = profile['Provider_Name_Prefix_Text']+profile['Provider_First_Name']+" "+profile['Provider_Last_Name_Legal_Name']
    if profile['Provider_Name_Suffix_Text']:
        narrative = narrative + " "+profile['Provider_Name_Suffix_Text']
    narrative = narrative + ".<br/>"
    narrative = narrative + "Tel:" + profile['Provider_Business_Practice_Location_Address_Telephone_Number']+"<br/>"
    narrative = narrative + "Practice Address:<br/>"
    narrative = narrative + profile['Provider_First_Line_Business_Practice_Location_Address']+"<br/>"
    if profile['Provider_Second_Line_Business_Practice_Location_Address']:
        narrative = narrative +profile['Provider_Second_Line_Business_Practice_Location_Address']+"<br/>"
    narrative = narrative + profile['Provider_Business_Practice_Location_Address_City_Name']+" "
    narrative = narrative + profile['Provider_Business_Practice_Location_Address_State_Name']+"<br/>"
    narrative = narrative + profile['Provider_Business_Practice_Location_Address_Postal_Code']+"<br/>"

    # if settings.DEBUG:
    #     print("Narrative function:", narrative)

    return narrative


def generate_fhir_profile(request, resourceType, src_dict ):
    """
    Receive a dictionary and convert to a profile. This will convert from
    input dictionary specific field names to the generic profile
    We can also build in some resourceType and input file specific logic
    :param request:
    :param resourceType: (We can use this as basis to pull a resource
            mapping if we make
    :param src_dict:
    :return: profile_dict

Profile elements:
    # Map values across to new dictionary
    npi['use']        = assign_str(source, 'use', "official")
    npi['type']       = assign_str(source, 'type',)
    npi['system']     = assign_str(source, 'system', sys_uri)
    *npi['value']      = assign_str(source, 'value',)
    npi['period']     = assign_str(source, 'period',)
    npi['assigner']   = assign_str(source, 'assigner', assigner_ref)

 * = Required

    """

    resource_map = {}

    fp = {}

    if settings.DEBUG:
        print("Source:", src_dict)

    # fp.update(src_dict)
    if not 'resourceType' in fp:
        if resourceType:
            fp['resourceType'] = resourceType

    if resourceType == "Practitioner":
        # Do Practitioner Specific mapping

        source = {}
        # Now we need to map NPI data in to the identifier segment
        source['value']= src_dict['NPI']
        if 'Replacement_NPI' in src_dict:
            # If a replacement NPI we need to use it
            if not src_dict['Replacement_NPI'] == "":
                source['value'] = src_dict['Replacement_NPI']

        # Let's set some dates:
        # Provider_Enumeration_Date = Date created. ie Period Start
        # NPI_Deactivation_Date = Period end date
        # If NPI_Reactivation_Date

        id_list = []
        if 'NPI_Reactivation_Date' in src_dict:
            if 'NPI_Deactivation_Date' in src_dict:
                if not src_dict['NPI_Deactivation_Date'] =="":
                    date_start = datetime.strptime(src_dict['Provider_Enumeration_Date'],"%m/%d/%Y")
                    date_end   = datetime.strptime(src_dict['NPI_Deactivation_Date'], "%m/%d/%Y")
                    source['period'] = {'start' : date_to_iso(date_start),
                                        'end' : date_to_iso(date_end)}
            id_list.append(npid(source))
            if src_dict['NPI_Reactivation_Date'] > src_dict['NPI_Deactivation_Date']:
                date_start = datetime.strptime(src_dict['NPI_Reactivation_Date'],"%m/%d/%Y")

                source['period'] = {'start' : date_to_iso(date_start)}

                id_list.append(npid(source))

        else:
            date_start = datetime.strptime(src_dict['Provider_Enumeration_Date'],"%m/%d/%Y")
            date_end   = datetime.strptime(src_dict['NPI_Deactivation_Date'], "%m/%d/%Y")

            source['period']['start'] = date_to_iso(date_start)
            if 'NPI_Deactivation_Date' in src_dict:
                if not src_dict['NPI_Deactivation_Date'] =="":
                    source['period']['end'] = date_to_iso(date_end)
            id_list.append(npid(source))

        fp['identifier'] = id_list

        # Now we need to map the name information to name

        #
        # hn['resourceType'] = "HumanName"
        # hn['use'] = assign_str(source, 'use', "usual")
        # hn['suffix'] = assign_str(source, 'suffix',)
        # hn['prefix'] = assign_str(source, 'prefix',)
        # hn['family'] = assign_str(source, 'family')
        # hn['given']  = assign_str(source, 'given')
        # hn['period'] = assign_str(source, 'period')

        name_source = {
                       'suffix' : [src_dict['Provider_Name_Suffix_Text'],
                                   src_dict['Provider_Credential_Text']],
                       'prefix' : src_dict['Provider_Name_Prefix_Text'],
                       'family' : [src_dict['Provider_Last_Name_Legal_Name']],
                       'given'  : [src_dict['Provider_First_Name'],
                                   src_dict['Provider_Middle_Name']]
                      }

        fp['fhir_human_name'] = human_name(name_source)

        # Now we need to map the contact information

        telecom_source =  {}
        tel_list = []
        # Map values across to new dictionary
        # cp['resourceType'] = "ContactPoint"
        # cp['system'] = assign_str(source, 'system', "usual")
        # cp['value']  = assign_str(source, 'value',)
        # cp['use']    = assign_str(source, 'use')
        # cp['rank']   = int(assign_str(source, 'rank'))
        # cp['period'] = assign_str(source, 'period')

        rank = 1
        if not src_dict['Provider_Business_Practice_Location_Address_Telephone_Number'] == "":
            telecom_source['system'] = "phone"
            telecom_source['value']  = src_dict['Provider_Business_Practice_Location_Address_Telephone_Number']
            telecom_source['use']    = "practice"
            telecom_source['rank']   = str(rank)

            tel_list.append(contact_point(telecom_source))
            rank += 1

        if not src_dict['Provider_Business_Practice_Location_Address_Fax_Number'] == "":
            telecom_source['system'] = "fax"
            telecom_source['value']  = src_dict['Provider_Business_Practice_Location_Address_Fax_Number']
            telecom_source['rank']   = str(rank)

            tel_list.append(contact_point(telecom_source))
            rank += 1

        if not src_dict['Provider_Business_Mailing_Address_Telephone_Number'] == "":
            telecom_source['system'] = "phone"
            telecom_source['value']  = src_dict['Provider_Business_Mailing_Address_Telephone_Number']
            telecom_source['use']    = "business"
            telecom_source['rank']   = str(rank)

            tel_list.append(contact_point(telecom_source))
            rank += 1

        if not src_dict['Provider_Business_Mailing_Address_Fax_Number'] == "":
            telecom_source['system'] = "fax"
            telecom_source['value']  = src_dict['Provider_Business_Mailing_Address_Fax_Number']
            telecom_source['rank']   = str(rank)

            tel_list.append(contact_point(telecom_source))

        fp['fhir_contact_point'] = tel_list

        # Now we need to map the address information

        addr_source = {}

        addr_list = []
        rank = 1

        # ad['resourceType'] = "Address"
        # ad['use']        = assign_str(source, 'use',)
        # ad['type']       = assign_str(source, 'type',)
        # ad['line']       = assign_str(source, 'line',)
        # ad['city']       = assign_str(source, 'city',)
        # ad['district']   = assign_str(source, 'district',)
        # ad['state']      = assign_str(source, 'state',)
        # ad['postalCode'] = assign_str(source, 'postalCode',)
        # ad['country']    = assign_str(source, 'country',)
        # ad['period']     = assign_str(source, 'period',)

        addr_source['use']   = "practice"
        addr_source['type']  = "physical"
        addr_source['line']  = [src_dict['Provider_First_Line_Business_Practice_Location_Address'],
                                src_dict['Provider_Second_Line_Business_Practice_Location_Address']]
        addr_source['city']  = src_dict['Provider_Business_Practice_Location_Address_City_Name']
        addr_source['state'] = src_dict['Provider_Business_Practice_Location_Address_State_Name']
        addr_source['postalCode'] = src_dict['Provider_Business_Practice_Location_Address_Postal_Code']
        addr_source['country'] = src_dict['Provider_Business_Practice_Location_Address_Country_Code_If_outside_US']

        addr_list.append(address(addr_source))

        addr_source['use']   = "business"
        addr_source['type']  = "postal"
        addr_source['line']  = [src_dict['Provider_First_Line_Business_Mailing_Address'],
                                src_dict['Provider_Second_Line_Business_Mailing_Address']]
        addr_source['city']  = src_dict['Provider_Business_Mailing_Address_City_Name']
        addr_source['state'] = src_dict['Provider_Business_Mailing_Address_State_Name']
        addr_source['postalCode'] = src_dict['Provider_Business_Mailing_Address_Postal_Code']
        addr_source['country'] = src_dict['Provider_Business_Mailing_Address_Country_Code_If_outside_US']

        addr_list.append(address(addr_source))

        fp['fhir_address'] = addr_list

        # Get Gender

        fp['gender'] = src_dict['Provider_Gender_Code']

        # Get User readable text
        fp['narrative'] = write_practitioner_narrative(src_dict)

        fp['fhir_extension'] = npi_provider_extension(src_dict)

    return fp


def npi_provider_extension(source):
    """
    Add non empty fields in NPI Record to NPI Extension in Practitioner
    Profile
    :param source:
    :return: profile['extension'] {}

    """
    extn = {}

    for key, value in source.items():
        if isinstance(value, str):
            if value == "":
                pass
            else:
                extn[key] = value
        if isinstance(value, int):
            if value:
                extn[key] = value
            else:
                pass
        if isinstance(value, list):
            if len(value) > 0:
                extn[key] = value
            else:
                pass
        if isinstance(value, dict):
            if len(value) > 0:
                extn[key] = value

    extn_dict = {'url' : settings.FHIR_SERVER + "/StructureDefinition/NPI_Provider_Record",
                 'extension' : extn
                }

    return extn_dict