import datetime
import subprocess
import psycopg2


try:
    connection = psycopg2.connect(
        host="95.213.151.56",
        user="ruslan",
        password="phanuB2E",
        database="tg_bot"
    )

    with connection.cursor() as cursor:
        cursor.execute('SELECT * FROM public.\"Domains\" ORDER BY id ASC')
        domains = cursor.fetchall()

        for domain in domains:
            domain_id = domain[0]
            date_now = datetime.datetime.now()

            check = subprocess.run(['ping', '-c', '1', domain[2]], capture_output=True, text=True)

            if check.returncode == 0:
                cursor.execute('INSERT INTO public.\"Ping\" (domain, date, access) VALUES (%s, %s, %s)', (domain_id, date_now, True))
            else:
                cursor.execute('INSERT INTO public.\"Ping\" (domain, date, access) VALUES (%s, %s, %s)',
                                (domain_id, date_now, False))

            connection.commit()

except Exception as ex:
    print("Err: ", ex)

finally:
    if connection:
        connection.close()
