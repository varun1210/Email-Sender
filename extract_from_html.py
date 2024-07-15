from lxml import etree
import pandas as pd
import application_configs

html_file_path = ''
with open(html_file_path, 'r', encoding='utf-8') as file:
    html_content = file.read()


parser = etree.HTMLParser()
tree = etree.fromstring(html_content, parser)

recruiter_mode = application_configs.RECRUITER_MODE
mode = application_configs.MODE

counter = 1

general_negative = [
    ["global"],
    # ["director"],
    # ["vp"],
    ["scien"],
    ["finan", "analy"],
    ["data center"]
]

swe_negative = [
    ["support", "enginee"],
    ["qa"],
    ["quality", "assurance"],
    ["site", "reliability"]
]

data_negative = [
    ["qa"],
    ["quality", "assurance"],
    ["support", "enginee"],
    ["site", "reliability"],
    ["quality"],
]


data_combos = [
    # ["data", "analy"],
    # ["data", "analy", "senior"],
    ["data", "anly", "manager"],
    ["data", "analy", "lead"],
    ["data", "analy", "head"],
    ["data", "analy", "principal"],
    ["data", "analy", "director"],
    # ["data", "enginee"],
    # ["data", "enginee", "senior"],
    ["data", "enginee", "manager"],
    ["data", "enginee", "lead"],
    ["data", "enginee", "head"],
    ["data", "enginee", "principal"],
    ["data", "enginee", "director"],
    # ["analy", "enginee"],
    # ["analy", "enginee", "senior"],
    ["analy", "enginee", "manager"],
    ["analy", "enginee", "lead"],
    ["analy", "enginee", "head"],
    ["analy", "enginee", "principal"],
    ["analy", "enginee", "director"],
    # ["busin", "intelligence", "enginee"],
    # ["busin", "intelligence", "senior"],
    ["busin", "intelligence", "manager"],
    ["busin", "intelligence", "lead"],
    ["busin", "intelligence", "head"],
    ["busin", "intelligence", "principal"],
    ["busin", "intelligence", "director"],
    # ["data"],
]

data_combos_upper = [
    # ["BI", "analy"],
    # ["BI", "analy", "senior"],
    ["BI", "analy", "manager"],
    ["BI", "analy", "lead"],
    ["BI", "analy", "head"],
    ["BI", "analy", "principal"],
    ["BI", "analy", "director"],
    # ["BI", "enginee"],
    # ["BI", "enginee", "senior"],
    ["BI", "enginee", "manager"],
    ["BI", "enginee", "lead"],
    ["BI", "enginee", "head"],
    ["BI", "enginee", "principal"],
    ["BI", "enginee", "director"],
    # ["ETL", "develop"],
    # ["ETL", "enginee"],
    ["ETL", "manager"],
    ["ETL", "lead"],
    ["ETL", "head"],
    ["ETL", "principal"],
    ["ETL", "director"],
]

recruiter_combos_negative = [
    ["global"],
    ["head"],
    ["manager"],
    ["director"],
    ["vp"],
    ["offshore"]
]

recruiter_combos_positive = [
    ["talent"],
    ["recruit"],
    ["sourcer"],
    ["technical", "recruiter"],
    ["talent", "sourcer"],
    ["talent", "acquisition"]
]


swe_combos = [
    # ["software", "engineer"],
    # ["software", "develop"],
    # ["backend", "engineer"],
    # ["senior", "software"],
    ["swe"],
    ["lead", "swe"],
    # ["senior", "swe"],
    ["software", "manager", "engineer"],
    ["swe", "manager"],
    ["lead", "engineer"],
    ["lead", "swe"],
    ["principal", "software"],
    ["head", "software"],
    ["head", "swe"],
    ["backend", "manager"],
    ["backend", "lead"],
    ["principal", "backend"],
    ["engineer", "manager"],
    # ["senior", "backend"],
    ["sde"],
    # ["senior", "sde"],
    ["manager", "sde"],
    ["principal", "sde"],
    # ["software"],
    # ["data"]
]

try:
    
    people = []
    fail_count = 0
    while True:
        name_xpath = "/html/body/div[4]/div[3]/div/div[2]/div/div[2]/main/div[2]/div/div[2]/div/div[1]/ul/li[{counter}]/div/section/div/div/div[2]/div[1]/a/div".format(counter=counter)
        designation_xpath = "/html/body/div[4]/div[3]/div/div[2]/div/div[2]/main/div[2]/div/div[2]/div/div[1]/ul/li[{counter}]/div/section/div/div/div[2]/div[3]/div/div".format(counter=counter)
        name_elements = tree.xpath(name_xpath)
        designation_elements = tree.xpath(designation_xpath)
        if not name_elements:
            fail_count += 1
            counter += 1
            if fail_count < 150:
                continue
            else: 
                break
        if not designation_elements:
            fail_count += 1
            counter += 1
            if fail_count < 150:
                continue
            else: 
                break
        name_text_content = ''
        designation_text_content = ''
        

        for element in name_elements:
            name_text_content = ''.join(element.xpath(".//text()")).strip()
        for element in designation_elements:
            designation_text_content = ''.join(element.xpath(".//text()")).strip()

        def contains_word_combos(text, combos, lower):
            if(lower):
                text = text.lower()
            for combo in combos:
                if all(word in text for word in combo):
                    return True
            return False
        
        if(recruiter_mode):
            if contains_word_combos(designation_text_content, recruiter_combos_positive) and not contains_word_combos(designation_text_content, recruiter_combos_negative):
                people.append(tuple([name_text_content, designation_text_content]))
        else:
            if mode == "DE":
                if (contains_word_combos(designation_text_content, data_combos, True) or contains_word_combos(designation_text_content, data_combos_upper, False)) and not contains_word_combos(designation_text_content, general_negative, True) and not contains_word_combos(designation_text_content, data_negative, True):
                    people.append(tuple([name_text_content, designation_text_content]))
            else:
                if contains_word_combos(designation_text_content, swe_combos, True) and not contains_word_combos(designation_text_content, general_negative, True) and not contains_word_combos(designation_text_content, swe_negative, True):
                    people.append(tuple([name_text_content, designation_text_content]))
        counter += 1
except Exception as e:
    print(e)
finally:
    people_df = pd.DataFrame(people, columns=['Name', 'Designation'])
    people_df.to_excel('./names.xlsx', index=False)

    