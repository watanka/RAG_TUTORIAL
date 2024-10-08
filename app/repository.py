from abc import ABC, abstractmethod
import sqlite3
import boto3
from botocore.exceptions import ClientError

class DB(ABC):
    @abstractmethod
    def save_email(self, email: str) -> None:
        pass

    @abstractmethod
    def get_emails(self) -> list:
        pass

    @abstractmethod
    def delete_email(self):
        pass

class SQLiteEmailDatabase(DB):
    def __init__(self, db_name: str = "emails.db"):
        self.conn = sqlite3.connect(db_name)
        self.create_table()

    def create_table(self):
        with self.conn:
            self.conn.execute(
                "CREATE TABLE IF NOT EXISTS emails (id INTEGER PRIMARY KEY, email TEXT UNIQUE)"
            )

    def save_email(self, email: str) -> None:
        with self.conn:
            self.conn.execute("INSERT INTO emails (email) VALUES (?)", (email,))

    def get_emails(self) -> list:
        cursor = self.conn.cursor()
        cursor.execute("SELECT email FROM emails")
        return [row[0] for row in cursor.fetchall()]

    def delete_email(self, email: str):
        with self.connection:
            self.connection.execute(
                "DELETE FROM emails WHERE email = ?", (email,)
            )
    def close(self):
        if self.conn:
            self.conn.close()

class DynamoDBEmailDatabase(DB):
    def __init__(self, table_name: str):
        self.table_name = table_name
        self.dynamodb = boto3.resource('dynamodb')
        self.table = self.dynamodb.Table(self.table_name)
        self.create_table()

    def create_table(self):
        try:
            self.dynamodb.create_table(
                TableName=self.table_name,
                KeySchema=[
                    {
                        'AttributeName': 'email',
                        'KeyType': 'HASH'  # Partition key
                    }
                ],
                AttributeDefinitions=[
                    {
                        'AttributeName': 'email',
                        'AttributeType': 'S'  # String
                    }
                ],
                ProvisionedThroughput={
                    'ReadCapacityUnits': 1,
                    'WriteCapacityUnits': 1
                }
            )
        except ClientError as e:
            if e.response['Error']['Code'] != 'ResourceInUseException':
                raise

    def save_email(self, email: str) -> None:
        self.table.put_item(Item={'email': email})

    def get_emails(self) -> list:
        response = self.table.scan()
        return [item['email'] for item in response.get('Items', [])]

    def delete_email(self, email):
        self.table.delete_item(Key={'email': email})

class EmailRepository:
    def __init__(self, db: DB):
        self.db = db

    def save_email(self, email: str) -> None:
        self.db.save_email(email)

    def get_emails(self) -> list:
        return self.db.get_emails()
    
    def remove_emails(self, email: str) -> None:
        self.db.delete_email(email)
    

if __name__ == '__main__':
    db = SQLiteEmailDatabase()
    repo = EmailRepository(db)

    repo.save_email('eunsung.shin@gmail.com')

    print('eunsung.shin@gmail.com' in repo.get_emails())