import pandas as pd
import streamlit as st
from google.cloud import secretmanager
import gspread
from google.oauth2.service_account import Credentials
import json

def planilha():
# GCP project in which to store secrets in Secret Manager.
    project_id = "luckjpa"

    # ID of the secret to create.
    secret_id = "Cred"

    # Create the Secret Manager client.
    secret_client = secretmanager.SecretManagerServiceClient()

    secret_name = f"projects/{project_id}/secrets/{secret_id}/versions/latest"
    response = secret_client.access_secret_version(request={"name": secret_name})

    secret_payload = response.payload.data.decode("UTF-8")

    credentials_info = json.loads(secret_payload)

    scopes = ["https://www.googleapis.com/auth/spreadsheets"]

    # Use the credentials to authorize the gspread client
    credentials = Credentials.from_service_account_info(credentials_info, scopes=scopes)
    client = gspread.authorize(credentials)

    spreadsheet = client.open_by_key('1sc1kyv7x-pEygwYZRNRxhezLkJoFgShKFeFdUnfEsDk')

    sheet = spreadsheet.worksheet("Base")

    # Get all values from the sheet
    sheet_data = sheet.get_all_values()
    df = pd.DataFrame(sheet_data[1:], columns=sheet_data[0])

    return df


def salvar_planilha(df):
    project_id = "luckjpa"

    # ID of the secret to create.
    secret_id = "Cred"

    # Create the Secret Manager client.
    secret_client = secretmanager.SecretManagerServiceClient()

    secret_name = f"projects/{project_id}/secrets/{secret_id}/versions/latest"
    response = secret_client.access_secret_version(request={"name": secret_name})

    secret_payload = response.payload.data.decode("UTF-8")

    credentials_info = json.loads(secret_payload)

    scopes = ["https://www.googleapis.com/auth/spreadsheets"]

    # Use the credentials to authorize the gspread client
    credentials = Credentials.from_service_account_info(credentials_info, scopes=scopes)
    client = gspread.authorize(credentials)

    spreadsheet = client.open_by_key('1sc1kyv7x-pEygwYZRNRxhezLkJoFgShKFeFdUnfEsDk')

    sheet = spreadsheet.worksheet("Base")

    # Get all values from the sheet
    sheet_data = sheet.get_all_values()
    df_sheet = pd.DataFrame(sheet_data[1:], columns=sheet_data[0])

    limpar_dados = 'A:D'
    sheet.batch_clear([limpar_dados])

    data = [df.columns.values.tolist()] + df.values.tolist()

    sheet.update('A1', data)

