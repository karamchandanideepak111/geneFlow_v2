from django.db import models
from django.conf import settings
import mysql.connector
import json

# Create your models here.
class InstrumentData:

    @staticmethod
    def create_instrument(data):
        dbdetails = settings.DB_DETAILS 
        connection = mysql.connector.connect(
            host=dbdetails['host'],
            user=dbdetails['user'],
            password=dbdetails['password'],
            database=dbdetails['database'],
            port=dbdetails['port']
        )
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