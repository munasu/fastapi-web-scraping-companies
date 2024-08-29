from fastapi import FastAPI, HTTPException
import mysql.connector
from typing import Dict


def get_db_connection():
    cnx = mysql.connector.connect(
        host="localhost",
        user="root",
        database="project"
    )
    return cnx


app = FastAPI()



@app.get('/api/company')
def get_company():
    try:
        cnx = get_db_connection()
        cursor = cnx.cursor(dictionary=True)
        query = "SELECT * FROM company_list"
        cursor.execute(query)
        rows = cursor.fetchall()
        cursor.close()
        cnx.close()
        if not rows:
            raise HTTPException(
                status_code=404, detail="No company found matching the search criteria.")

        return rows
    except mysql.connector.Error as e:
        raise HTTPException(status_code=500, detail="Database error occurred.")
    finally:
        cursor.close()
        cnx.close()


@app.get('/api/juristic/{id}')
def get_juristic_id(id: str):
    try:
        cnx = get_db_connection()
        cursor = cnx.cursor(dictionary=True)
        query = "SELECT * FROM company_list WHERE juristic_id=%s"
        cursor.execute(query, (id,))
        rows = cursor.fetchall()

        if not rows:
            raise HTTPException(
                status_code=404, detail="No company found matching the search criteria.")

        return rows
    except mysql.connector.Error as e:
        raise HTTPException(status_code=500, detail="Database error occurred.")
    finally:
        cursor.close()
        cnx.close()


@app.get('/api/search')
def get_search_company(search: str):
    try:
        cnx = get_db_connection()
        cursor = cnx.cursor(dictionary=True)
        query = ("SELECT * FROM company_list WHERE company LIKE %s OR symbols LIKE %s "
                 "OR legal_entity_name LIKE %s")
        search_pattern = f"%{search}%"
        cursor.execute(query, (search_pattern, search_pattern, search_pattern))
        rows = cursor.fetchall()

        if not rows:
            raise HTTPException(
                status_code=404, detail="No company found matching the search criteria.")

        return rows
    except mysql.connector.Error as e:
        raise HTTPException(status_code=500, detail="Database error occurred.")
    finally:
        cursor.close()
        cnx.close()


@app.get('/api/compare')
def get_compare_company(company_1: str, company_2: str):
    try:
        cnx = get_db_connection()
        cursor = cnx.cursor(dictionary=True)

        query_1 = "SELECT * FROM company_list WHERE juristic_id = %s"
        cursor.execute(query_1, (company_1,))
        company_1_details = cursor.fetchone()

        query_2 = "SELECT * FROM company_list WHERE juristic_id = %s"
        cursor.execute(query_2, (company_2,))
        company_2_details = cursor.fetchone()

        if not company_1_details or not company_2_details:
            raise HTTPException(
                status_code=404, detail="One or both companies not found.")

        return {"company_1": company_1_details, "company_2": company_2_details}

    except mysql.connector.Error as e:
        raise HTTPException(status_code=500, detail="Database error occurred.")
    finally:
        cursor.close()
        cnx.close()
