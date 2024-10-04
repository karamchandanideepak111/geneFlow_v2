import mysql.connector
import json
import uuid
import pandas as pd
from django.conf import settings

class DatabaseConnection:
    @staticmethod
    def get_connection():
        dbdetails = settings.DB_DETAILS  
        connection = mysql.connector.connect(
            host=dbdetails['host'],
            user=dbdetails['user'],
            password=dbdetails['password'],
            database=dbdetails['database'],
            port=dbdetails['port']
        )
        return connection

class ConnectorData:
    @staticmethod
    def fetch_conn_data():
        connection = DatabaseConnection.get_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("""
            SELECT * 
            FROM geneflow.connDB AS c 
            JOIN geneflow.instrumentDB AS i 
            ON c.instrument_id = i.instrument_id;
        """)
        rows = cursor.fetchall()
        cursor.close()
        connection.close()
        return json.dumps(rows, indent=4, default=str)

    @staticmethod
    def register_connector(data):
        connection = DatabaseConnection.get_connection()
        cursor = connection.cursor()
        insert_query = "CALL insert_conn(%s, %s, %s)"
        connector_key = str(uuid.uuid4())
        cursor.execute(insert_query, (
            data['connector_name'],
            connector_key,
            data['instrument_id']
        ))
        connection.commit()
        cursor.close()
        connection.close()
        return ConnectorData.fetch_conn_data()

    @staticmethod
    def update_connector(data):
        connection = DatabaseConnection.get_connection()
        cursor = connection.cursor()
        update_query = """
            UPDATE geneflow.connDB 
            SET connector_name = %s, status = %s
            WHERE ckey = %s
        """
        cursor.execute(update_query, (
            data.get('connector_name'),
            data.get('status'),
            data.get('connector_key')
        ))
        connection.commit()
        cursor.close()
        connection.close()

    @staticmethod
    def delete_connector(connector_id):
        connection = DatabaseConnection.get_connection()
        cursor = connection.cursor()
        delete_query = "DELETE FROM geneflow.connDB WHERE connector_id = %s"
        cursor.execute(delete_query, (connector_id,))
        connection.commit()
        cursor.close()
        connection.close()

    @staticmethod
    def validate_connector(key):
        connection = DatabaseConnection.get_connection()
        cursor = connection.cursor(dictionary=True)
        conn_query = """
            SELECT * FROM geneflow.connDB AS c 
            JOIN geneflow.instrumentDB AS i 
            ON c.instrument_id = i.instrument_id 
            WHERE c.ckey = %s
        """
        cursor.execute(conn_query, (key,))
        result = cursor.fetchall()
        cursor.close()
        connection.close()
        return pd.DataFrame(result) if result else None

    @staticmethod
    def fetch_connector_and_instrument_data(conn_id, key):
        connection = DatabaseConnection.get_connection()
        cursor = connection.cursor(dictionary=True)
        conn_query = """
            SELECT * FROM geneflow.connDB AS c 
            JOIN geneflow.instrumentDB AS i 
            ON c.instrument_id = i.instrument_id 
            WHERE c.connector_id = %s AND c.ckey = %s
        """
        cursor.execute(conn_query, (conn_id, key))
        result = cursor.fetchall()
        cursor.close()
        connection.close()
        return pd.DataFrame(result)

    @staticmethod
    def insert_log(conn_id, instru_id, ip, hostname, timestamp, status, org_filename, new_file_name):
        connection = DatabaseConnection.get_connection()
        cursor = connection.cursor()
        insert_query = """
            CALL insert_logs (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(insert_query, (
            conn_id, instru_id, ip, hostname, timestamp, 
            status, org_filename, new_file_name
        ))
        connection.commit()
        cursor.close()
        connection.close()
