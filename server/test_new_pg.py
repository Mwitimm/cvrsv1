from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

app = Flask(__name__)

# PostgreSQL connection parameters
db_host = 'localhost'
db_port = 8000
db_name = 'test_postgre'
db_user = 'postgres'
db_password = 'admin'

# SQLAlchemy configuration
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Create a SQLAlchemy database instance
db = SQLAlchemy(app)

@app.route('/')
def index():
    try:
        # Check if the connection is successful by executing a raw SQL query
        db.session.execute(text('SELECT 1'))
        print("Connection to PostgreSQL database successful")
    except Exception as e:
        print("Error connecting to PostgreSQL database:", e)

    return "Check your console for connection status."

if __name__ == '__main__':
    app.run(debug=True)
