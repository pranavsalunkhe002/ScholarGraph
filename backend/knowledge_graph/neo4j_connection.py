import os
from neo4j import GraphDatabase
from dotenv import load_dotenv


# Load environment variables from .env
load_dotenv()


# Neo4j connection details
URI = os.getenv("NEO4J_URI")
USERNAME = os.getenv("NEO4J_USERNAME")
PASSWORD = os.getenv("NEO4J_PASSWORD")


# Create Neo4j driver
driver = GraphDatabase.driver(
    URI,
    auth=(USERNAME, PASSWORD)
)


def test_connection():
    try:
        with driver.session() as session:

            result = session.run(
                "RETURN 'ScholarGraph Neo4j Connection Successful!' AS message"
            )

            record = result.single()

            print(record["message"])

    except Exception as e:

        print("Neo4j connection failed!")
        print("Error:", e)


if __name__ == "__main__":
    test_connection()
    driver.close()