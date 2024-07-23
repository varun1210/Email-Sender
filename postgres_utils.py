import psycopg2

def insert_record_to_pg(postgres_details, data_tuple, user):
    conn = psycopg2.connect(
        dbname=postgres_details["dbname"],
        user=postgres_details["user"],
        password=postgres_details["password"],
        host=postgres_details["host"],
        port=postgres_details["port"]
    )
    if user == "Varun Muppalla":
        insert_query = 'INSERT INTO sent (name, company, employee_email_id, designation, time_sent) VALUES (%s, %s, %s, %s, %s);'
    else: 
        insert_query = 'INSERT INTO sent_maitrai (name, company, employee_email_id, designation, time_sent) VALUES (%s, %s, %s, %s, %s);'
    cursor = conn.cursor()
    cursor.execute(insert_query, data_tuple)
    conn.commit()
    cursor.close()
    conn.close()
    return

def get_record_count(postgres_details, user):
    conn = psycopg2.connect(
        dbname=postgres_details["dbname"],
        user=postgres_details["user"],
        password=postgres_details["password"],
        host=postgres_details["host"],
        port=postgres_details["port"]
    )
    cursor = conn.cursor()
    if user == "Varun Muppalla":
        cursor.execute(
            '''
            SELECT count(*) 
            FROM sent
            WHERE time_sent is NOT NULL and time_sent >= (CURRENT_TIMESTAMP - INTERVAL '1 day');
            '''
        )
    else:
        cursor.execute(
            '''
            SELECT count(*) 
            FROM sent_maitrai
            WHERE time_sent is NOT NULL and time_sent >= (CURRENT_TIMESTAMP - INTERVAL '1 day');
            '''
        )
    count = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    return count

def query_sent(postgres_details, employee_email):
    conn = psycopg2.connect(
        dbname=postgres_details["dbname"],
        user=postgres_details["user"],
        password=postgres_details["password"],
        host=postgres_details["host"],
        port=postgres_details["port"]
    )
    cursor = conn.cursor()
    cursor.execute(
        '''
        SELECT count(employee_email_id)
        FROM mailing_list
        WHERE employee_email_id = '{employee_email}'
        '''.format(employee_email=employee_email)
    )
    count = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    if count == 0:
        return False
    else:
        return True


