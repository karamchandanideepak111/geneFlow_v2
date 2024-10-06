from django.db import models
from django.conf import settings
import mysql.connector
import json

class DatabaseConnection:
    @staticmethod
    def get_connection():
        dbdetails = settings.DB_DETAILS  # Assuming you have DB details in settings
        connection = mysql.connector.connect(
            host=dbdetails['host'],
            user=dbdetails['user'],
            password=dbdetails['password'],
            database=dbdetails['database'],
            port=dbdetails['port']
        )
        return connection

class LogsManager(models.Manager):
    def fetch_logs_data(self):
        # Establish connection with MySQL database
        connection = DatabaseConnection.get_connection()

        cursor = connection.cursor(dictionary=True)

        # Query to fetch logs data
        cursor.execute("""
            SELECT DISTINCT log_id, connector_id, instrument_name, version, ip_address, pc_name, 
                            timestamp, status, org_filename, updated_filename 
            FROM geneflow.logsDB AS l 
            JOIN geneflow.instrumentDB AS i 
            ON l.instrument_id = i.instrument_id 
            ORDER BY log_id DESC;
        """)
        rows = cursor.fetchall()

        # Close cursor and connection
        cursor.close()
        connection.close()
        print("Total number of rows = ",len(rows))
        # Return the fetched data as JSON
        return json.dumps(rows, indent=4, default=str)

# Define a Logs model (you can expand this if you want Django ORM to work with this table)
class Logs(models.Model):
    objects = LogsManager()
