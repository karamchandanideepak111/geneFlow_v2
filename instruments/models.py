from django.db import models
import mysql.connector
import json
from django.conf import settings

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
    
# Create your models here.
class InstrumentData:
    @staticmethod
    def create_instrument(data):
        dbdetails = settings.DB_DETAILS 
        connection = DatabaseConnection.get_connection()
        cursor = connection.cursor()

        # Insert query for adding a new instrument into instrumentDB
        insert_query = "INSERT INTO instrumentDB (instrument_name, category, price) VALUES (%s, %s, %s)"
        
        # Execute the insert query with data from the POST request
        cursor.execute(insert_query, (
            data['instrument_name'],
            data['category'],
            data['price']
        ))

        # Commit the transaction
        connection.commit()

        # Close the cursor and connection
        cursor.close()
        connection.close()

        # Return all instruments after insertion to confirm success
        return json.dumps({ 'body':'Entered Successfully' }, indent=4)