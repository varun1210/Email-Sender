import os
import psycopg2
import pandas as pd
from auto import construct_email_to


conn = psycopg2.connect(
    dbname="email_sender",
    user=os.environ.get('EMAIL_SENDER_POSTGRES_USER'),
    password=os.environ.get('EMAIL_SENDER_POSTGRES_PASSWORD'),
    host="localhost",
    port=5433
)

insert_query = 'INSERT INTO mailing_list (employee_name, employee_company, employee_email_id, designation) VALUES (%s, %s, %s, %s);'
cursor = conn.cursor()

with open("./Blast.xlsx", 'rb') as file:
    names_df = pd.read_excel(file, sheet_name='Mailing_List')
    for index, row in names_df.iterrows():
        
        name = row['Name']
        name = name.strip()
        company = row['Company']
        company = company.strip()
        option = row['Option']
        designation = row['Designation']
        if designation == 'NOPE':
            designation = None
        if type(designation) == str and designation.strip() == '':
            designation = None
        if type(designation) != str:
            desingation = None
        employee_email_id = construct_email_to(option, name, company)
        if employee_email_id == None:
            continue
        insert_tuple = (name, company, employee_email_id, designation)
        cursor.execute(insert_query, insert_tuple)

conn.commit()
cursor.close()
conn.close()