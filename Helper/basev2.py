# Extract section based on title (for the second website)
def extract_section(soup, section_title):
    section_data = {}
    try:
        caption_div = soup.find('div', class_='Caption', string=section_title)
        if caption_div:
            info_table = caption_div.find_next('div', class_='InformationBoxTable')
            if info_table:
                rows = info_table.find_all('div', class_='InformationBoxRow')
                for row in rows:
                    title = row.find('div', class_='InformationBoxTitle').text.strip()
                    content = row.find('div', class_='InformationBoxContents').text.strip()
                    section_data[title] = content
    except Exception as e:
        print(f"Error extracting section {section_title}: {e}")
    return section_data

# Extract data from the second website
def extract_all_data(soup):
    data = {}
    data['General Data'] = extract_section(soup, 'General Data')
    data['Personal Data'] = extract_section(soup, 'Personal Data')
    data['Career Data'] = extract_section(soup, 'Career Data')
    return data





