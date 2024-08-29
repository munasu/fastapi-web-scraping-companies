import mysql.connector
from selenium import webdriver
import pandas as pd
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import os
from dotenv import load_dotenv

load_dotenv()

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        database="project"
    )


def fetch_companies():
    cnx = get_db_connection()
    cursor = cnx.cursor()
    query = "SELECT id, company FROM company_list WHERE id > 567"
    cursor.execute(query)
    rows = cursor.fetchall()
    cursor.close()
    cnx.close()
    return [{"id": row[0], "company": row[1]} for row in rows]


companies = fetch_companies()

driver = webdriver.Chrome()

results = []

try:
    driver.get('https://data.creden.co/')
    time.sleep(5)
    driver.find_element(
        By.XPATH, '/html/body/div[1]/div/div/div/div[4]/div/div/div[1]/button').click()
    time.sleep(5)
    driver.find_element(
        By.XPATH, "/html/body/div[1]/div/div/div/div[1]/div[1]/div/div[3]/div/div[6]/a").click()
    time.sleep(5)

    email_input = driver.find_element(
        By.XPATH, "/html/body/div[1]/div/div/div/div/div[1]/input")
    email_input.send_keys(os.getenv("EMAIL_ACCOUNT"))
    password_input = driver.find_element(
        By.XPATH, "/html/body/div[1]/div/div/div/div/div[1]/div[2]/input")
    password_input.send_keys(os.getenv("PASSWORD_ACCOUNT"))
    password_input.send_keys(Keys.RETURN)
    time.sleep(5) 

    for count, item in enumerate(companies):
        if count != 0:
            driver.get('https://data.creden.co/')
        time.sleep(5)
        driver.find_element(
            By.XPATH, '/html/body/div[1]/div/div/div/div[4]/div/div/div[1]/button').click()
        time.sleep(5)

        company = item["company"]

        juristic_input = driver.find_element(
            By.XPATH, "/html/body/div[1]/div/div/div/div[2]/div[2]/div/div/input")
        juristic_input.send_keys(company)
        time.sleep(5)
        juristic_input.send_keys(Keys.RETURN)
        time.sleep(5)

        try:
            driver.find_element(
                By.XPATH, "/html/body/div[1]/div/div/div/div[2]/div/div[3]/div/div/h3")
            continue  
        except:
            pass

        try:
            company_link = driver.find_element(
                By.XPATH, "/html/body/div[1]/div/div/div/div[2]/div/div[4]/div[1]/div/h3/a")
            driver.execute_script(
                "arguments[0].removeAttribute('target')", company_link)
            company_link.click()
            time.sleep(5)
            
            try:
                dialog_id = driver.find_element(
                    By.XPATH,"/html/body/div[1]/div/div/div/div[8]/div/div/div[1]/button")
                dialog_id.click()
                time.sleep(5)
            except:
                pass

            juristic_id = driver.find_element(
                By.XPATH, "/html/body/div[1]/div/div/div/div[4]/div/div[3]/div[1]/div/div/table/tbody/tr[1]/td").text

            total_income = driver.find_element(
                By.XPATH, "/html/body/div/div/div/div/div[4]/div/div[1]/div[1]/div/div[1]/div/div/div/h4").text.replace(",", "").strip()

            total_income_percentage = driver.find_element(
                By.XPATH, "/html/body/div/div/div/div/div[4]/div/div[1]/div[1]/div/div[1]/div/div/div/h5").text.replace("YoY", "").replace("%", "").replace(",", "").strip()

            net_profit = driver.find_element(
                By.XPATH, "/html/body/div/div/div/div/div[4]/div/div[1]/div[2]/div/div[1]/div/div/div/h4").text.replace(",", "").strip()

            net_profit_percentage = driver.find_element(
                By.XPATH, "/html/body/div/div/div/div/div[4]/div/div[1]/div[2]/div/div[1]/div/div/div/h5").text.replace("YoY", "").replace("%", "").replace(",", "").strip()

            total_assets = driver.find_element(
                By.XPATH, "/html/body/div[1]/div/div/div/div[4]/div/div[1]/div[3]/div/div[1]/div/div/div/h4").text.replace(",", "").strip()

            total_assets_percentage = driver.find_element(
                By.XPATH, "/html/body/div/div/div/div/div[4]/div/div[1]/div[3]/div/div[1]/div/div/div/h5").text.replace("YoY", "").replace("%", "").replace(",", "").strip()

            current_registered_capital = driver.find_element(
                By.XPATH, "/html/body/div[1]/div/div/div/div[4]/div/div[3]/div[2]/div[2]/div/table/tbody/tr[1]/td").text.replace(",", "").strip()

            company_value = driver.find_element(By.XPATH, "/html/body/div[1]/div/div/div/div[4]/div/div[3]/div[2]/div[2]/div/table/tbody/tr[2]/td").text.replace(
                ",", "").replace("บาท", "").split("(", 1)[0].strip()

            legal_entity_name = driver.find_element(
                By.XPATH, "/html/body/div/div/div/div/div[4]/div/div[3]/div[1]/div/div/table/thead/tr/td").text

            try:
                old_legal_entity_id = driver.find_element(
                    By.XPATH, "/html/body/div/div/div/div/div[4]/div/div[3]/div[1]/div/div/table/tbody/tr[2]/th")
                if old_legal_entity_id.text == "เลขทะเบียนนิติบุคคล (เดิม)":
                    date_of_registration_xpath = "/html/body/div/div/div/div/div[4]/div/div[3]/div[1]/div/div/table/tbody/tr[4]/td"
                    business_status_xpath = "/html/body/div/div/div/div/div[4]/div/div[3]/div[1]/div/div/table/tbody/tr[5]/td/span"
                    business_type_xpath = "/html/body/div/div/div/div/div[4]/div/div[3]/div[1]/div/div/table/tbody/tr[6]/td"
                else:
                    raise Exception()
            except:
                date_of_registration_xpath = "/html/body/div/div/div/div/div[4]/div/div[3]/div[1]/div/div/table/tbody/tr[3]/td"
                business_status_xpath = "/html/body/div/div/div/div/div[4]/div/div[3]/div[1]/div/div/table/tbody/tr[4]/td/span"
                business_type_xpath = "/html/body/div/div/div/div/div[4]/div/div[3]/div[1]/div/div/table/tbody/tr[5]/td"

            date_of_registration = driver.find_element(
                By.XPATH, date_of_registration_xpath).text.split("(", 1)[0].strip()
            business_status = driver.find_element(
                By.XPATH, business_status_xpath).text.split(" ")[0]
            business_type = driver.find_element(
                By.XPATH, business_type_xpath).text

            # Save to the database
            update_cnx = get_db_connection()
            update_cursor = update_cnx.cursor()
            sql_update_query = """
                UPDATE company_list 
                SET 
                    juristic_id = %s, 
                    total_income = %s, 
                    total_income_percentage = %s, 
                    net_profit = %s, 
                    net_profit_percentage = %s, 
                    total_assets = %s, 
                    total_assets_percentage = %s, 
                    current_registered_capital = %s, 
                    company_value = %s, 
                    legal_entity_name = %s, 
                    date_of_registration = %s, 
                    business_status = %s, 
                    business_type = %s 
                WHERE id = %s
            """
            update_data = (
                juristic_id, total_income, total_income_percentage, net_profit, net_profit_percentage,
                total_assets, total_assets_percentage, current_registered_capital, company_value,
                legal_entity_name, date_of_registration, business_status, business_type, item[
                    "id"]
            )
            update_cursor.execute(sql_update_query, update_data)
            update_cnx.commit()
            update_cursor.close()
            update_cnx.close()

            results.append({
                "id": item["id"],
                "company": company,
                "juristic_id": juristic_id,
                "total_income": total_income,
                "total_income_percentage": total_income_percentage,
                "net_profit": net_profit,
                "net_profit_percentage": net_profit_percentage,
                "total_assets": total_assets,
                "total_assets_percentage": total_assets_percentage,
                "current_registered_capital": current_registered_capital,
                "company_value": company_value,
                "legal_entity_name": legal_entity_name,
                "date_of_registration": date_of_registration,
                "business_status": business_status,
                "business_type": business_type
            })

        except Exception as e:
            print(f"An error occurred while processing {company}: {e}")

finally:
    file_exists = os.path.isfile("company_juristic_ids.csv")
    df = pd.DataFrame(results)

    if file_exists:
        df.to_csv("company_juristic_ids.csv",
                  mode='a', header=False, index=False)
    else:
        df.to_csv("company_juristic_ids.csv", index=False)

    driver.quit()
