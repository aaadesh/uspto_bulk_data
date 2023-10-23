from bs4 import BeautifulSoup
from tqdm import tqdm
import sqlite3


#SQL Part here:

conn = sqlite3.connect('patents_database.db')
cursor = conn.cursor()

create_table_sql = """
CREATE TABLE IF NOT EXISTS Patent_Table (
    "Patent" TEXT PRIMARY KEY,
    "Publication Number" TEXT,
    "Country Code" TEXT,
    "Patent Number" TEXT,
    "Kind Code" TEXT,
    "Application" TEXT,
    "Application Country Code" TEXT,
    "Application Number" TEXT,
    "Publication Date" TEXT,
    "Application Date" TEXT,
    "Title" TEXT,
    "First Claim" TEXT,
    "Claims" TEXT,
    "Description" TEXT,
    "US Citations" TEXT
)
"""

cursor.execute(create_table_sql)



def read_patent(patent):
    
    soup = BeautifulSoup(patent, 'html.parser')
    #print(soup)

    clm = soup.find("claim", {"num" : "00001"})
    if clm != None:
        first_claim = clm.text
        #print(first_claim)
    else:
        first_claim = None
    
    all_claims = []
    clms = soup.find_all("claim")
    if clms is not None:
        for claim in clms:
            all_claims.append(claim.text)
            #print(claim.text)
    claims = " ".join(all_claims)
    
    des = soup.find("description", {"id" : "description"})
    if des != None:
        description = des.text
        #print(description)
    else:
        description = "N/A"
    
    if soup.find("publication-reference") is not None:
        cc = soup.find("publication-reference").find("country").text
        num = soup.find("publication-reference").find("doc-number").text
        kind = soup.find("publication-reference").find("kind").text
        pub_date = soup.find("publication-reference").find("date").text
        patent = cc + num
        patentk = cc + num + kind
        #print(cc, num, patent, pub_date)
    
    app_cc = "N/A"
    app_num = "N/A"
    app_date = "N/A"
    app = "N/A"
    
    if soup.find("application-reference") is not None: 
        app_cc = soup.find("application-reference").find("country").text
        app_num = soup.find("application-reference").find("doc-number").text
        app_date = soup.find("application-reference").find("date").text
        app = app_cc + app_num
        #print(app, app_date)
    
    tit = soup.find("invention-title").text if soup.find("invention-title") is not None else "N/A"
    #print(tit)
    
    us_citations = []
    npl_cit = "N/A"
    citation_number = "N/A"
    citation_num =  "N/A"
    citation_cc =  "N/A"
    citation_name =  "N/A"
    citation_date = "N/A"
    citation_cat =  "N/A"
    citation_number = "N/A"
    us_citations_combined = "N/A"
    
    cit = soup.find_all("us-citation")
    if len(cit) != 0:
        #print(cit)
        for c in cit:
            if c.find("country") is not None:
                citation_num =  c.find("doc-number").text if c.find("doc-number") is not None else "N/A"
                citation_cc =  c.find("country").text if c.find("country") is not None else "N/A"
                citation_name =  c.find("name").text if c.find("name") is not None else "N/A"
                citation_date =  c.find("date").text if c.find("date") is not None else "N/A"
                citation_cat =  c.find("category").text if c.find("category") is not None else "N/A"
                citation_number = citation_cc + citation_num
                
                #print(citation_cc, citation_date, citation_name, citation_num, citation_cat)
            if c.find("nplcit") is not None:
                npl_cit = c.find("othercit").text if c.find("othercit") is not None else "N/A"
                #print(npl_cit)
            #if npl_cit is not None:
            citation_combined = citation_number + " " + citation_cc + " " + citation_date + " " + citation_name + " " + citation_num + " " + citation_cat + " " + npl_cit
            #else:
                #citation_combined = citation_number + " " + citation_cc + " " + citation_date + " " + citation_name + " " + citation_num + " " + citation_cat
                
            us_citations.append(citation_combined)
        us_citations_combined = " | ".join(us_citations)
        #print(us_citations_combined)
        
       
    #cpc = soup.find_all("classifications-cpc")
    #print(cpc)
    #if len(cpc) != 0:
        
    data = {
        "Patent": patent,
        "Publication Number": patentk,
        "Country Code": cc,
        "Patent Number": num,
        "Kind Code": kind,
        
        "Application": app,
        "Application Country Code": app_cc,
        "Application Number": app_num,
        
        "Publication Date": pub_date,
        "Application Date": app_date,
        
        "Title": tit,
        "First Claim": first_claim,
        "Claims": claims,
        "Description": description,
        "US Citations": us_citations_combined,
                
    }
    #print(data)
    
    data_values = (
    data['Patent'],
    data['Publication Number'],
    data['Country Code'],
    data['Patent Number'],
    data['Kind Code'],
    data['Application'],
    data['Application Country Code'],
    data['Application Number'],
    data['Publication Date'],
    data['Application Date'],
    data['Title'],
    data['First Claim'],
    data['Claims'],
    data['Description'],
    data['US Citations']
    )
    
    existing_patent = cursor.execute("SELECT * FROM Patent_Table WHERE Patent = ?", (data['Patent'],)).fetchone()

    if existing_patent:

        update_sql = """
        UPDATE Patent_Table
        SET "Publication Number" = ?,
            "Country Code" = ?,
            "Patent Number" = ?,
            "Kind Code" = ?,
            "Application" = ?,
            "Application Country Code" = ?,
            "Application Number" = ?,
            "Publication Date" = ?,
            "Application Date" = ?,
            "Title" = ?,
            "First Claim" = ?,
            "Claims" = ?,
            "Description" = ?,
            "US Citations" = ?
        WHERE Patent = ?
        """
        cursor.execute(update_sql, (data['Publication Number'], data['Country Code'], data['Patent Number'], data['Kind Code'], data['Application'], data['Application Country Code'], data['Application Number'], data['Publication Date'], data['Application Date'], data['Title'], data['First Claim'], data['Claims'], data['Description'], data['US Citations'], data['Patent']))
    else:
        # No existing record with the same "Patent" value; insert a new record
        sql = 'INSERT INTO Patent_Table ("Patent", "Publication Number", "Country Code", "Patent Number", "Kind Code", "Application", "Application Country Code", "Application Number", "Publication Date", "Application Date", "Title", "First Claim", "Claims", "Description", "US Citations") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'
        cursor.execute(sql, data_values)

    
    #sql = 'INSERT INTO Patent_Table ("Patent", "Publication Number", "Country Code", "Patent Number", "Kind Code", "Application", "Application Country Code", "Application Number", "Publication Date", "Application Date", "Title", "First Claim", "Claims", "Description", "US Citations") VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'

    #cursor.execute(sql, data_values)

    #for field_name, field_value in data.items():
        #cursor.execute("INSERT OR REPLACE INTO Patent_Table (FieldName, FieldValue) VALUES (?, ?)", (field_name, field_value))
    


xml_file_path = "D:\Database\Grant\ipg231010.xml"
xml_file_path = repr(xml_file_path)[1:-1]

#split and read the individual patents
with open(xml_file_path) as f:
        xml = f.read()
all_patents = xml.split('<?xml version="1.0" encoding="UTF-8"?>')
all_patents = all_patents[1:]

#read_patent(all_patents[5000])

#for patent in all_patents:
    #read_patent(patent)
    #print("patent processed:")

#print(all_patents[6000])
#print(len(all_patents))


for patent in tqdm(all_patents, desc="Processing patents", unit="patent"):
    read_patent(patent)
    #print("patent processed:")


conn.commit()
conn.close()