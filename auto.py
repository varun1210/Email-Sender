import os
import pandas as pd
import constants
import application_configs
import postgres_utils
import datetime
import time
import json

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.utils import formataddr


def initialize_state(file_path):
    person_list = []
    with open(file_path, 'rb') as file:
        names_df = pd.read_excel(file, sheet_name='Sheet1')
        for _, row in names_df.iterrows():
            person_list.append(tuple([row['Name'], row['Company'], row['Option'], row['Designation']]))
    return person_list

def construct_email_to(option, name, company):
    if(name == 'Varun Muppalla'):
        return "varunm1210@gmail.com"
    
    with open("./email_format_meta.json", "r") as file:
        special_companies = json.load(file)

    if('(' in name or ')' in name or "'" in name or '"' in name):
        return None 
    
    name_cleaner1 = {
        "á" : "a",
        "é" : "e",
        "è" : "e",
        "ñ" : "n",
        "ǹ" : "n",
        "ń" : "n",
        "SAFe®5" : "",
        "Ed.S" : "",
        "Ed.S." : "",
        "SAFe" : "",
        "CGMA" : "",
        "CERA" : "",
        "CSPO" : "",
        "PSPO" : "",
        "SPC" : "",
        "SPHR" : "",
        "SHRM-CSP" : "",
        "AIPMM" : "",
        "SP" : "",
        "Jr." : "",
        "jr." : "",
        "Sr." : "",
        "sr." : "",
        "Dr." : "",
        "dr." : "",
        "AIS" : "",
        "AU" : "",
        "SCPM" : "",
        "CPMA" : "",
        "POPM" : "",
        "CIPM" : "",
        "CPM" : "",
        "PMP" : "",
        "APM" : "",
        "PM" : "",
        "BCMAS" : "",
        "CPMA" : "",
        "MAAA" : "",
        "CISA" : "",
        "CSAM" : "",
        "FSA" : "",
        "MA" : "",
        "M.A." : "",
        "m.a." : "",
        "ASA" : "",
        "SA" : "",
        "CSPO" : "",
        "PSPO" : "",
        "POPM" : "",
        "PO" : "",
        "." : "",
        "," : "",
        "®" : ""
    }
    
    name = name.strip()
    for item in sorted(name_cleaner1, key=len, reverse=True):
        if(item in name):
            name = name.replace(item, name_cleaner1[item]).strip()

    restricted_names = constants.RESTRICTED_NAMES
    restricted_names = sorted(restricted_names, key=len, reverse=True)

    name = name.lower().strip()

    for item in restricted_names:
        verify_string = ' ' + item
        if(verify_string in name):
            name = name.replace(verify_string, '')

    name = name.strip()
    domain = "com"

    if(company.strip() in special_companies):
        company_info = special_companies[company.strip()]
        if "domain" in company_info:
            domain = company_info["domain"]
        company = company_info["company"]
    else:
        company = company.replace(' ', '').lower().strip()
    
    first_name = name.split(' ')[0].strip().replace('.', '').replace('®', '')
    last_name = name.split(' ')[-1].strip().replace('.', '').replace('®', '')

    if(',' in first_name or ',' in last_name or '-' in first_name or '-' in last_name):
        return None

    if(len(last_name) == 1 and option in [1, 2, 6, 7, 8, 11, 13, 14, 15]):
        return None
    
    if(len(first_name) == 1 and option in [1, 3, 4, 7, 8, 9, 10, 14, 15]):
        return None
    
    match option:

         # max.tell@company.com
        case 1:
            return "{first_name}.{last_name}@{company}.{domain}".format(first_name=first_name, last_name=last_name, company=company, domain=domain)
    
        # mtell@company.com
        case 2:
            return "{first_initial}{last_name}@{company}.{domain}".format(first_initial=first_name[0], last_name=last_name, company=company, domain=domain) 
    
        # max@company.com
        case 3:
            return "{first_name}@{company}.{domain}".format(first_name=first_name, last_name=last_name, company=company, domain=domain)  
        
        # tmax@company.com
        case 4:
            return "{last_initial}{first_name}@{company}.{domain}".format(last_initial=last_name[0], first_name=first_name, company=company, domain=domain)  
    
        # m.t@company.com    
        case 5:
            return "{first_initial}.{last_initial}@{company}.{domain}".format(first_initial=first_name[0], last_initial=last_name[0], company=company, domain=domain)  

        # tell@company.com
        case 6:
            return "{last_name}@{company}.{domain}".format(last_name=last_name, company=company, domain=domain)
        
        # max_tell@company.com
        case 7: 
            return "{first_name}_{last_name}@{company}.{domain}".format(first_name=first_name, last_name=last_name, company=company, domain=domain)
        
        # maxtell@company.com
        case 8: 
            return "{first_name}{last_name}@{company}.{domain}".format(first_name=first_name, last_name=last_name, company=company, domain=domain)
        
        # maxt@company.com
        case 9: 
            return "{first_name}{last_initial}@{company}.{domain}".format(first_name=first_name, last_initial=last_name[0], company=company, domain=domain)

        # max.t@company.com
        case 10:
            return "{first_name}.{last_initial}@{company}.{domain}".format(first_name=first_name, last_initial=last_name[0], company=company, domain=domain)
        
        # m.tell@company.com
        case 11:
            return "{first_initial}.{last_name}@{company}.{domain}".format(first_initial=first_name[0], last_name=last_name, company=company, domain=domain)
        
        # mxtell@company.com
        case 12:
            return "{first_inital}x{last_name}@{company}.{domain}".format(first_initial=first_name[0], last_name=last_name, company=company, domain=domain)
        
        # tellm@company.com
        case 13:
            return "{last_name}{first_initial}@{company}.{domain}".format(last_name=last_name, first_initial=first_name[0], company=company, domain=domain)
        
        # tell_max@company.com
        case 14: 
            return "{last_name}_{first_name}@{company}.{domain}".format(last_name=last_name, first_name=first_name, company=company, domain=domain)
        
        # max-tell@company.com
        case 15:
            return "{first_name}-{last_name}@{company}.{domain}".format(first_name=first_name, last_name=last_name, company=company, domain=domain) 


def bulk_send(person_list, user, postgres_details):
    enable_rate_limiter = False
    if len(person_list) > 30:
        enable_rate_limiter = True
        rate_limiter_count = 0

    for person in person_list:
        name = person[0].strip()
        first_name = name.split(' ')[0].strip()
        if first_name == "Dr." or first_name == "dr.":
            first_name = name.split(' ')[1].strip()
        first_name = first_name[0].upper() + first_name[1:].lower()
        last_name = name.split(' ')[-1].strip()
        last_name = last_name[0].upper() + last_name[1:].lower()
        company = person[1].strip()
        option = person[2]
        designation = person[3]
        email_to = construct_email_to(option, name, company)
        if not email_to:
            continue
        sent_flag = postgres_utils.query_sent(postgres_details, email_to)
        if sent_flag:
            print("Email already sent to: {email}".format(email=email_to))
            continue
        message = MIMEMultipart()
        message['From'] = formataddr((user, email_from))
        message['To'] = email_to
        message['Subject'] = email_subject.format(company=company)
        message.attach(MIMEText(email_body.format(first_name=first_name, company=company), 'plain'))
        
        with open(resume_path, 'rb') as file:
            part = MIMEApplication(file.read(), Name=user.replace(" ", "_") + "_Resume.pdf")
            part['Content-Disposition'] = 'attachment; filename="{filename}"'.format(filename=user.replace(" ", "_") + "_Resume.pdf")
            message.attach(part)
        
        try:
            if(enable_rate_limiter and rate_limiter_count > 0 and rate_limiter_count % 30 == 0):
                print("Sent {sent}. Sleeping....".format(sent=rate_limiter_count))
                time.sleep(30)

            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls() 
            server.login(email_from, email_password) 
            sent_in_last_24_hrs = postgres_utils.get_record_count(postgres_details, user)
            if (sent_in_last_24_hrs > 490):
                print("Reached threshold record")
                break
            server.sendmail(email_from, email_to, message.as_string())
            data_tuple = (name, company, email_to, designation, datetime.datetime.now())
            postgres_utils.insert_record_to_pg(postgres_details, data_tuple, user)
            print("Email sent to: {name}".format(name=name))
            server.quit()
            if enable_rate_limiter:
                rate_limiter_count += 1
        except Exception as e:
            print("Email send failed for: {name}".format(name=name))
            raise e


if __name__ == "__main__":
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587

    user = application_configs.USER
    recruiter = application_configs.RECRUITER_MODE
    mode = application_configs.MODE
    postgres_details = application_configs.POSTGRES_CREDENTIALS
    postgres_details["user"] = os.environ.get('EMAIL_SENDER_POSTGRES_USER')
    postgres_details["password"] = os.environ.get('EMAIL_SENDER_POSTGRES_PASSWORD')
    file_path = "./Blast.xlsx"

    if user == 'Varun Muppalla':

        if mode == "SWE":
            email_subject = constants.SWE_EMAIL_SUBJECT
            email_body = constants.SWE_EMAIL_BODY
            resume_path = constants.SWE_RESUME_PATH
        else:
            email_subject = constants.DE_EMAIL_SUBJECT
            email_body = constants.DE_EMAIL_BODY
            resume_path = constants.DE_RESUME_PATH

        if recruiter and mode == "DE":
            email_subject = constants.RECRUITER_EMAIL_SUBJECT_DE
            email_body = constants.RECRUITER_EMAIL_BODY_DE

        if recruiter and mode == "SWE":
            pass

        email_from = os.environ.get('EMAIL_SENDER_EMAIL_VARUN')
        email_password = os.environ.get('EMAIL_SENDER_PASSWORD_VARUN')
        person_list = initialize_state(file_path)
        bulk_send(person_list, user, postgres_details)
        
    else:
        email_from = os.environ.get('EMAIL_SENDER_EMAIL_MAITRAI')
        email_password = os.environ.get('EMAIL_SENDER_PASSWORD_MAITRAI')
        email_subject = constants.MAITRAI_EMAIL_SUBJECT
        email_body = constants.MAITRAI_EMAIL_BODY
        resume_path = constants.MAITRAI_RESUME_PATH
        person_list = initialize_state(file_path)
        bulk_send(person_list, user, postgres_details)