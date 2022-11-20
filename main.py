from bs4 import BeautifulSoup
import requests
import pandas as pd
import logging





def validate_string(negeri_sample, parlimen_sample):
    if '-' in negeri_sample:
        clean_negeri_name = negeri_sample.replace("-", " ")

    if '-' in parlimen_sample:
        clean_parlimen_name = parlimen_sample.replace("-", " ")

    return clean_negeri_name, clean_parlimen_name

    
def create_data():
    negeri = "pulau-pinang"
    parlimen = "tasek-gelugor"
    
    headers = ['negeri', 'parlimen', 'calon', 'parti/gabungan', 'undi', 'majoriti']
    df = pd.DataFrame(columns = headers)

    url = f"https://www.myundi.com.my/pru15/{negeri}/parlimen/{parlimen}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    election_result_table = soup.find("div", class_= "row mt-4")
    candidate_count = len(election_result_table.find_all("div", class_="stitle d-flex align-items-center justify-content-between"))
    election_result_table_second_level = election_result_table.find_all("div", class_="stitle d-flex align-items-center justify-content-between")[1]


    for i in range(candidate_count):
        election_result_table_second_level = election_result_table.find_all("div", class_="stitle d-flex align-items-center justify-content-between")[i]

        calon = [election_result_table_second_level.find("div", class_="col-lg-4 text-left").get_text()]
        parti = [election_result_table_second_level.find("span", class_="text-uppercase").get_text()]
        undi_table = election_result_table_second_level.find("div", class_="col-lg-3 text-right")
        undi_table_tag = undi_table.find_all('p')
        result_number_length = len(undi_table_tag)

        if result_number_length > 1:
            for i in range(result_number_length):
                undi = [undi_table_tag[1].find('b').get_text()]
                majoriti = [undi_table_tag[2].find('b').get_text()]
        else:
            undi = [undi_table_tag[0].find('b').get_text()]
            majoriti = [None]

        negeri_cleaned, parlimen_cleaned = validate_string(negeri, parlimen)


        complete_data = [negeri_cleaned] + [parlimen_cleaned] + calon + parti + undi + majoriti

        length = len(df)

        df.loc[length] = complete_data
        
    df.to_csv(f'{parlimen}.csv', index=False)

if __name__ == "__main__":
    logging.basicConfig(level = logging.INFO)

    try:
        create_data()
        logging.info("File is created")
    except Exception as e:
        logging.info(f"{e}")