#============================Importations des librairies===============================
import requests
from bs4 import BeautifulSoup
import random
from tqdm import tqdm
import re
import pandas as pd
from datetime import datetime
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

#===============================constantes==============================================


liste_url = ["https://www.amazon.fr/Google-Pixel-Smartphone-dautonomie-Volcanique/dp/B0D7TYVYRY/ref=sr_1_5?crid=11Y36HE2OHNO5&dib=eyJ2IjoiMSJ9.EGkr3YvIIGj-Wz0pal0bSLq8LxPn5wezt6PUdxEXcpoTvGi8Q9qsSqlvDlenckIuWs1Wp_iYzkFLX0TxIvqozN1uG50MWkeLoF88miF9HvVSZF-NeDMsbfDpOOit7Zux9qs2NUXEUEj18uDjHBBYIY_kUE-eQWW6nO1AKf0w-V2ngoRJO8U2smzu7t95Sk5SAf_XYd1-m0ZRvlLcwMtLAWuHe1yaiMYrg5V31SBvdGcl6Z2tpF0VzYRjdpQc2sCboh9Rn_ySLyWAA5QGiyU6zTreoNj6Y70Zy4fQAZ_rOSGIV3A21M1BZ8oKe7uLnZyysRgP1VvKQaIC0hteMpjSUDy67UPVeecJGkeCpJF1gZk.w0MfATPSWmYJ3mFJfxt6G07CvMOU-p7fr_KiicEsBTM&dib_tag=se&keywords=google%2Bpixel&qid=1739734394&s=electronics&sprefix=goo%2Celectronics%2C982&sr=1-5&th=1",
             "https://www.amazon.fr/Apple-iPhone-Pro-Max-256/dp/B0DGHR9VG2/ref=sr_1_3_sspa?__mk_fr_FR=%C3%85M%C3%85%C5%BD%C3%95%C3%91&crid=3EHDD6E64DYDB&dib=eyJ2IjoiMSJ9.4NDNEv4NrQYOOnbgtXOZ7k3NKd95Efk2L6w64SQLI2vxoIRk_kqLA01vPN24qm0HwQ_09XbwPTs7_MdIYyaL30gF--40Pj7VFAjlP1VN2Cv_SG3kWCgtDFeQE7QSAjl0v39xGi2txM84Vb_kTP36BwjMoiIPuhdMGys1HLPrztcorX4s-BOeZ5BwRBLOcovFNWy_JFACoqksLtXHzZrqJ7jqy0mctKr0GeyU2xlkED1ePbRRg0Q7Dq7_ztRiibs3Hfx_cd1m9wRLJv955JhLzQGnpwpNhNHWQcOhDFAZvzg.DrCwO4wkq6qQ3vGNF7A6KsGEQvRZK2jaKtE1lfusJvY&dib_tag=se&keywords=Apple&qid=1739733779&s=electronics&sprefix=apple%2Celectronics%2C912&sr=1-3-spons&sp_csd=d2lkZ2V0TmFtZT1zcF9hdGY&th=1",
             "https://www.amazon.fr/gp/aw/d/B0DNZKMV8J/?_encoding=UTF8&pd_rd_plhdr=t&aaxitk=8d75d5ae80bd9387f4f135f737a4cf47&hsa_cr_id=0&qid=1739731849&sr=1-1-e0fa1fdd-d857-4087-adda-5bd576b25987&ref_=sbx_be_s_sparkle_lsi4d_asin_0_title&pd_rd_w=FB76K&content-id=amzn1.sym.fcb06097-6196-4e78-932c-0f6f89d56105%3Aamzn1.sym.fcb06097-6196-4e78-932c-0f6f89d56105&pf_rd_p=fcb06097-6196-4e78-932c-0f6f89d56105&pf_rd_r=HP77Y46K2ZAYZR56YPYX&pd_rd_wg=PvpQz&pd_rd_r=40bcef69-c83f-48d5-9a59-b5cb96b0ad29&th=1",
             #"https://www.amazon.fr/Google-Pixel-Smartphone-dautonomie-Volcanique/dp/B0D7TYVYRY/ref=sr_1_5?crid=11Y36HE2OHNO5&dib=eyJ2IjoiMSJ9.EGkr3YvIIGj-Wz0pal0bSLq8LxPn5wezt6PUdxEXcpoTvGi8Q9qsSqlvDlenckIuWs1Wp_iYzkFLX0TxIvqozN1uG50MWkeLoF88miF9HvVSZF-NeDMsbfDpOOit7Zux9qs2NUXEUEj18uDjHBBYIY_kUE-eQWW6nO1AKf0w-V2ngoRJO8U2smzu7t95Sk5SAf_XYd1-m0ZRvlLcwMtLAWuHe1yaiMYrg5V31SBvdGcl6Z2tpF0VzYRjdpQc2sCboh9Rn_ySLyWAA5QGiyU6zTreoNj6Y70Zy4fQAZ_rOSGIV3A21M1BZ8oKe7uLnZyysRgP1VvKQaIC0hteMpjSUDy67UPVeecJGkeCpJF1gZk.w0MfATPSWmYJ3mFJfxt6G07CvMOU-p7fr_KiicEsBTM&dib_tag=se&keywords=google%2Bpixel&qid=1739734394&s=electronics&sprefix=goo%2Celectronics%2C982&sr=1-5&th=1",
             #"https://www.amazon.fr/Google-Pixel-Smartphone-d%C3%A9bloqu%C3%A9-renouvel%C3%A9/dp/B09LR34Z3C/ref=sr_1_3?crid=DG79WXUHCJKA&dib=eyJ2IjoiMSJ9.EGkr3YvIIGj-Wz0pal0bSLq8LxPn5wezt6PUdxEXcpoTvGi8Q9qsSqlvDlenckIuWs1Wp_iYzkFLX0TxIvqozN1uG50MWkeLoF88miF9HvVSZF-NeDMsbfDpOOit7Zux9qs2NUXEUEj18uDjHBBYIY_kUE-eQWW6nO1AKf0w-V2ngoRJO8U2smzu7t95Sk5SAf_XYd1-m0ZRvlLcwMtLAWuHe1yaiMYrg5V31SBvdGcl6Z2tpF0VzYRjdpQc2sCboh9Rn_ySLyWAA5QGiyU6zVDD2J30l0Nl2__JhYLlzpg.-doq8M-d1DVlZgyc3ZOxX0hXBE6B1XChPWU7kYaE77Q&dib_tag=se&keywords=google+pixel&qid=1739734657&s=electronics&sprefix=google+pixel%2Celectronics%2C1978&sr=1-3",
             "https://www.amazon.fr/HUAWEI-fonctionnalit%C3%A9s-Ultra-Rapide-T%C3%A9l%C3%A9objectif-Supercharge/dp/B0CZ3J1PT7/ref=sr_1_1_sspa?__mk_fr_FR=%C3%85M%C3%85%C5%BD%C3%95%C3%91&dib=eyJ2IjoiMSJ9.FHr3Uoscg38h0ur1yC6BuYYFOLSjjK294UxW6jkY10yZvQA0eBW3g_hwS9oJG07MxkEqwHcb-FgbAP1b8YmZuK8p8gTpUvP-kbnk0U_pAGj3xjaS3P1hu0p8T6NwKjQC8mgQws0S6CrHoBzOAnAJAurpsNRBIcTQ0Hk-Iet2CM_p1XhD-14aVBDSezE8uifnddLqEV08TgDd5-mF86MHyInAmBwtacnD6m146HH4M62xIru8WPERMQsMgpK3sOTETu2hrkVjfxkTIT3hBmeSDxTNKwPm4SeG2l1aObKiKfQ.Uhw8QS2BROjGbtYFQ6yKRVE8TQTuvl57qZRv48nI7OY&dib_tag=se&keywords=Huawei&qid=1739753355&s=electronics&sr=1-1-spons&sp_csd=d2lkZ2V0TmFtZT1zcF9hdGY&psc=1",
             "https://www.amazon.fr/Xiaomi-T%C3%A9l%C3%A9phone-portable-Processeur-batterie/dp/B0DNYYJWQV/ref=sr_1_2_sspa?__mk_fr_FR=%C3%85M%C3%85%C5%BD%C3%95%C3%91&dib=eyJ2IjoiMSJ9.oyc8gOIkMnC8VPQlc4sIERH_gDdgJ5MXJ9fpk1T_CFZc26TqRi0dhfuL2LgMsspF5jRBRCp0UJrLgcy_ANO7kpOUdRADLHWbQVN7-tVTJgv0kEdzLNO3ENxKRLOePAtOkVWbsUeBdAuGJLI68zRW2qNCXL1yb35gRb4aJgQ4oAjOejWWAeAePxrV4kNQSZb8iRQBaVsTqHfUEushlE033D38XsHizVKw8uwlaJU8bsNhSID9SFm28KoLyNQaHWRlqv18zI1HG4C7cZgofT6OX7pVXEPBUNbtVBpbtZ5NUUc.rIQamMAQOYbAbXVJuWzJkegntLzTKd11wLzVXRLKwN0&dib_tag=se&keywords=Xiaomi%2BRedmi&qid=1739755204&sr=8-2-spons&sp_csd=d2lkZ2V0TmFtZT1zcF9hdGY&th=1"]



#============================Fonctions==================================================

# Fonction pour scraper Amazon
def scrape_amazon(url):
    headers = {
        "User-Agent": random.choice([
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        ])
    }

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        return f"Erreur {response.status_code}: Impossible d'accéder à la page"

    soup = BeautifulSoup(response.text, "html.parser")

    # Récupérer le titre
    title_tag = soup.find("span", {"id": "productTitle"})
    title = title_tag.text.strip() if title_tag else "Titre non trouvé"

    # Récupérer l'image principale
    image_tag = soup.find("img", {"id": "landingImage"})
    image_url = image_tag["src"] if image_tag and "src" in image_tag.attrs else "Image non trouvée"

    # Récupérer le prix
    price_tag = soup.find("span", {"class": "a-price-whole"})
    price = price_tag.text.strip() if price_tag else "Prix non trouvé"

    # Récupérer les évaluations (Note et nombre de votes)
    rating_tag = soup.find("span", {"class": "a-icon-alt"})
    rating = rating_tag.text.strip() if rating_tag else "Évaluation non trouvée"

    # Nombre de votes
    review_count_tag = soup.find("span", {"id": "acrCustomerReviewText"})
    review_count = review_count_tag.text.strip() if review_count_tag else "Nombre de votes non trouvé"

    price_cents_tag = soup.find("span", {"class": "a-price-fraction"})
    price_cents = price_cents_tag.text.strip() if price_cents_tag else "00"

    currency_tag = soup.find("span", {"class": "a-price-symbol"})
    currency = currency_tag.text.strip() if currency_tag else None # Default to euro if not found

    return {
        "Titre": title,
        "Image": image_url,
        "Prix entier": price,
        "Prix cents": price_cents,
        "Évaluation": rating,
        "Nombre d'évaluations": review_count,
        #"Prix": f"{price}{price_cents}", # Combined price
        "Monnaie": currency,
    }


def scrape_liste_url(liste_urls,list_base=liste_url):
  liste_resultats=[]
  retry_list=[]
  t=0
  for i in tqdm(liste_urls):
      a=scrape_amazon(i)
      try:
        if a["Titre"]=="Titre non trouvé":
            retry_list.append(i)
        else:
            a["Numero_Item"]=list_base.index(i)
            liste_resultats.append(a)
      except Exception as e:
        #retry_list.append(i)
        print(e)
        continue
        #retry_list.append(i)
  print(len(retry_list))
  #print(retry_list)
  if len(retry_list)==0:
    return liste_resultats
  return liste_resultats+scrape_liste_url(retry_list)


def clean_evaluation(df):
    # Clean 'Évaluation' column
    df['Evaluation'] = df['Évaluation'].astype(str)
    df['Evaluation'] = df['Evaluation'].str.extract(r'(\d+(?:,\d+)?)', expand=False).str.replace(',', '.')
    df['Evaluation'] = pd.to_numeric(df['Evaluation'], errors='coerce')
    #f["base_evaluations"] = df["Évaluation"].str.extract(r'( (\d+)?)', expand=False)
    # Clean 'Nombre d'évaluations' column
    df['Nombre_d_evaluations'] = df["Nombre d'évaluations"].astype(str)
    df['Nombre_d_evaluations'] = df['Nombre_d_evaluations'].str.replace(r'[^\d]', '', regex=True)
    df['Nombre_d_evaluations'] = pd.to_numeric(df['Nombre_d_evaluations'], errors='coerce').fillna(0).astype(int)

    return df


# Function to clean and convert price to integer (updated for cents)
def clean_price(row):
    try:
        price_entier = re.sub(r'[^\d.]', '', row['Prix entier'])
        price_cents = re.sub(r'[^\d.]', '', row['Prix cents'])
        return float(price_entier + '.' + price_cents)
    except (ValueError, TypeError, KeyError):
        return None


def clean_df(df):
  df1=clean_evaluation(df)
  df1['Prix'] = df1.apply(clean_price, axis=1)
  columns_to_drop = ['Prix entier', 'Prix cents',"Nombre d'évaluations",'Évaluation']
  df1 = df1.drop(columns=columns_to_drop, errors='ignore')
  return df1



def compare_and_append_dataframes(df, df1):
    """Compares df and df1, appends rows from df to df1 if needed, and returns changes."""
    changes = ""
    price_changes = ""

    # Convert 'Numero_Item' to numeric if it's not already. Handle potential errors gracefully.
    try:
        df['Numero_Item'] = pd.to_numeric(df['Numero_Item'], errors='coerce')
        df1['Numero_Item'] = pd.to_numeric(df1['Numero_Item'], errors='coerce')
    except KeyError:
        print("Warning: 'Numero_Item' column not found in one or both DataFrames.")
        return df1, None  # Return None for changes if 'Numero_Item' is missing

    for index, row in df.iterrows():
        item_number = row['Numero_Item']

        # Find the most recent entry for the corresponding item in df1
        try:
            most_recent_df1 = df1[df1['Numero_Item'] == item_number].sort_values(by="Date", ascending=False).iloc[0]
        except IndexError:
            # No matching item found in df1
            df1 = pd.concat([df1, pd.DataFrame([row])], ignore_index=True)
            new_title=row["Titre"]
            changes += f"New item detected with index {item_number} and title: \n\t {new_title}.\n"
            continue

        # Compare if observations are different
        if not row.drop('Date').equals(most_recent_df1.drop('Date')):
            # Append the observation from df to df1
            df1 = pd.concat([df1, pd.DataFrame([row])], ignore_index=True)
            changes += f"Changes detected for item with index {item_number}:\n"
            for col in row.index:
                if col != "Date" and col != 'Numero_Item' and row[col] != most_recent_df1[col]:
                    changes += f"  - {col}: {most_recent_df1[col]} -> {row[col]}\n"
            # Specific check for price changes
            if row['Prix'] != most_recent_df1['Prix']:
                price_changes += f"Price changed for item {item_number}: {most_recent_df1['Prix']} -> {row['Prix']}\n"


    if changes or price_changes:
      if price_changes:
        changes += "\nPrice change details:\n" + price_changes
      return df1, changes
    else:
      return df1, None



def send_email_with_csv(changes, receiver_email="nostatsum@gmail.com", csv_file_path='amazon_products.csv'):
    sender_email = "nostatsum@gmail.com"#"projetwebscrapping@gmail.com"  # Replace with your email
    sender_password = "pqlp qqtr epvf chkj"  # Replace with your email password (or app password)

    msg = MIMEMultipart()
    msg["Subject"] = "Amazon Price Tracker: Changes Detected"
    msg["From"] = sender_email
    msg["To"] = receiver_email

    # Add the text part of the email
    msg.attach(MIMEText(changes, "plain"))

    # Add the CSV attachment
    with open(csv_file_path, "rb") as attachment:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())
    encoders.encode_base64(part)
    part.add_header(
        "Content-Disposition",
        f"attachment; filename= {csv_file_path}",
    )
    msg.attach(part)


    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error sending email: {e}")


#================Procédure==============================================


p=scrape_liste_url(liste_url)


# Assuming 'p' is the list of dictionaries you obtained from scrape_liste_url
df = pd.DataFrame(p)

# Add a 'Date' column with today's date
df['Date'] = datetime.now().strftime('%Y-%m-%d')
df=clean_df(df)
#df

# Check if the file exists
file_path = 'amazon_products.csv'
if os.path.exists(file_path):
  df1 = pd.read_csv(file_path)
  print(df1.head()) # Print first 5 lines
else:
  df1=pd.DataFrame(columns=df.columns)
  print(f"The file '{file_path}' does not exist.")

DF2,letter=compare_and_append_dataframes(df, df1)
DF2

list_receiver_mail=["rdometi205@gmail.com"]
if letter:  # Check if there are changes
    letter=letter + "\n new_base attached"
    DF2.to_csv('amazon_products.csv', index=False) # Save the updated dataframe
    for i in list_receiver_mail:
        send_email_with_csv(letter,receiver_email=i)
    #send_email_with_csv(letter)
else:
    print("No changes detected.")
