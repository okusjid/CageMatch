
# Extract table data (for the first website)
def extract_table(soup):
    try:
        table_div = soup.find('div', class_='Table')
        if table_div:
            return table_div.find('div', class_='TableContents')
    except Exception as e:
        print(f"Error extracting table: {e}")
    return None

# Extract rows from the table (for the first website)
def extract_table_rows(table_contents):
    rows_data = []
    try:
        if table_contents:
            rows = table_contents.find_all('tr', class_='TRow1')
            for row in rows:
                row_data = {}
                columns = row.find_all('td')
                if len(columns) > 0:
                    row_data['Gimmick'] = columns[1].text.strip()
                    row_data['Birthday'] = columns[2].text.strip()
                    row_data['Birthplace'] = columns[3].text.strip()
                    row_data['Height'] = columns[4].text.strip()
                    row_data['Weight'] = columns[5].text.strip()
                    promotion = columns[6].find('img')
                    if promotion:
                        row_data['Promotion'] = promotion.get('alt')
                    row_data['Rating'] = columns[7].text.strip()
                    row_data['Votes'] = columns[8].text.strip()
                rows_data.append(row_data)
                break
    except Exception as e:
        print(f"Error extracting table rows: {e}")
    return rows_data
