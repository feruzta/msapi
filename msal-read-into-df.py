import requests
from msal import ConfidentialClientApplication
import pandas as pd
from io import BytesIO

tenant_id = "TENANT-ID"
client_id = "CLIENT-ID"
client_secret = "CLIENT-SECRET"
authority = f"https://login.microsoftonline.com/{tenant_id}"
site_url = "pthpam.sharepoint.com:/sites/TimData"

app = ConfidentialClientApplication(client_id, authority=authority, client_credential=client_secret)
token_response = app.acquire_token_for_client(scopes=["https://graph.microsoft.com/.default"])

if "access_token" not in token_response:
    print("Failed to retrieve token:", token_response)
    exit()

token = token_response["access_token"]
headers = {"Authorization": "Bearer " + token}
drive_id = "b!DGzrhjoRS0SURi9dB3X6hZ7cBgilx8dDg89O7mO0pk-JzX9MOAErSpXd3qQAIuv0"
file_id = "01VUCGGEAWWLF3HTZV3NGKCRKH3LXAE3UX"  # master_kpd.xlsx

# Download and Read "master_kpd.xlsx" into a DataFrame
response = requests.get(f"https://graph.microsoft.com/v1.0/drives/{drive_id}/items/{file_id}/content", headers=headers)
if response.status_code == 200:
    df_kpd = pd.read_excel(BytesIO(response.content))
    print("Excel file read into DataFrame successfully!")
    print(df.head())  # Display the first 5 rows of the DataFrame
else:
    print("Failed to download Excel file:", response.status_code)
    print(response.text)
