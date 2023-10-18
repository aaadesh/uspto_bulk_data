from bs4 import BeautifulSoup
from tqdm import tqdm


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
            all_claims.append(claim)
            #print(claim.text)
    
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

    
    if soup.find("application-reference") is not None: 
        app_cc = soup.find("application-reference").find("country").text
        app_num = soup.find("application-reference").find("doc-number").text
        app_date = soup.find("application-reference").find("date").text
        appk = app_cc + app_num
        #print(appk, app_date)
    
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

for patent in tqdm(all_patents, desc="Processing patents", unit="patent"):
    read_patent(patent)
    #print("patent processed:")

#print(all_patents[6000])
#print(len(all_patents))



