import time
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import Select
import pandas as pd
import numpy as np

driver = webdriver.Chrome(r'D:\scraping\chromedriver.exe')  # Optional argument, if not specified will search path.
driver.get('https://www.cwb.gov.tw/V8/C/D/UVIHistory.html')

time.sleep(2)

select = Select(driver.find_element_by_id('Date'))   #selecting the options from the drop_down form
op_D = []
for op in select.options:
    if op.text == '2018 / 12':
        break
    else:
        op_D.append(op.text)
print(op_D)

for i in range(len(op_D)):
    select.select_by_index(i)
    time.sleep(2)
    soup = BeautifulSoup(driver.page_source, features="html.parser")
    data = soup.find('table', id="UVIHistory_MOD")
    columns = [th.text.replace('\n', '') for th in data.find('tr').find_all('th')][1:]

    # date
    tbody = data.find('tbody')
    ths = tbody.find_all('tr')[:]
    rows_d = []
    for tr in ths:
        rows_d.append([th.text.replace('\n', '').replace('\xa0', '') for th in tr.find_all('th')])
        rows_D = np.reshape(rows_d, (len(rows_d), 1))

    # uvi
    trs = data.find_all('tr')[1:]
    rows = list()
    for tr in trs:
        rows.append([td.text.replace('\n', '').replace('\xa0', '') for td in tr.find_all('td')])

    for row in range(len(rows)):
        # print(row)
        df = pd.DataFrame(data=[rows[row]], columns=columns)    #save to DataFrame by date
        # print(df.head())
        df['Date'] = rows_D[row]
        print(df.head())

        op_D = [i.replace(' / ', '') for i in op_D]

        print(f'UVI_{op_D[i]+str(rows_D[row])[10:12]}.csv')
        df.to_csv(f'UVI_{op_D[i]+str(rows_D[row])[10:12]}.csv')

driver.quit()
