from lxml import etree
import pandas as pd
import application_configs

html_file_path = './(3) StubHub_ People _ LinkedIn.html'

with open(html_file_path, 'r', encoding='utf-8') as file:
    html_content = file.read()


parser = etree.HTMLParser()
tree = etree.fromstring(html_content, parser)

recruiter_mode = application_configs.RECRUITER_MODE

counter = 1

general_negative = [
    ["global"],
    ["director"],
    ["vp"],
    ["scien"],
    ["finan", "analy"],
    ["data center"]
]


data_combos = [
    # ["data", "engineer"],
    ["data", "manager", "engineer"],
    ["data", "engineer", "head"],
    ["data", "engineer", "lead"],
    ["data", "engineer", "principal"],
    # ["data", "analyst"],
    # ["analytics", "engineer"],
    # ["senior", "data"],
    # ["intelligence", "engineer"],
    ["lead", "intelligence", "busin"],
    # ["senior", "intelligence", "busin"],
    # ["senior", "analy", "data"],
    ["analy", "manager", "data"],
    ["intelligence", "manager", "busi"],
    ["lead", "analy"],
    ["lead", "data"],
    ["principal", "data"],
    ["head", "data"],
    ["principal", "intelligence"],
    ["principal", "analy", "data"],
    ["head", "analy", "data"],
    ["analy", "engineer", "manager"],
    ["analy", "engineer", "head"], 
    ["analy", "engineer", "lead"],
    ["analy", "engineer", "principal"],
    # ["senior", "analy", "engineer"],
    # ["analy"],
    # ["data"],
    ["lead", "bi", "analy"],
    ["head", "bi", "analy"],
    ["principal", "bi", "analy"],
    ["manage", "bi", "analy"],
    # ["senior", "bi", "analy"],
    ["lead", "bi", "engineer"],
    ["head", "bi", "engineer"],
    ["manage", "bi", "engineer"],
    ["principal", "bi", "engineer"],
    # ["senior", "bi", "engineer"],
    ["data", "engineer", "manager"],
    # ["senior", "data", "engineer"],
    # ["senior", "data", "analyst"],
]


recruiter_combos_negative = [
    ["global"],
    ["head"],
    ["manager"],
    ["director"],
    ["vp"]
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
    ["software", "engineer"],
    ["software", "develop"],
    ["backend", "engineer"],
    ["senior", "software"],
    ["swe"],
    ["lead", "swe"],
    ["senior", "swe"],
    ["software", "manager"],
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
    ["senior", "backend"],
    ["sde"],
    ["senior", "sde"],
    ["manager", "sde"],
    ["principal", "sde"]
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

        def contains_word_combos(text, combos):
            text_lower = text.lower()
            for combo in combos:
                if all(word in text_lower for word in combo):
                    return True
            return False
        
        if(recruiter_mode):
            if contains_word_combos(designation_text_content, recruiter_combos_positive) and not contains_word_combos(designation_text_content, recruiter_combos_negative):
                people.append(tuple([name_text_content, designation_text_content]))
        else:
            if contains_word_combos(designation_text_content, data_combos) and not contains_word_combos(designation_text_content, general_negative):
                people.append(tuple([name_text_content, designation_text_content]))

        
        

        counter += 1
except Exception as e:
    print(e)
finally:
    people_df = pd.DataFrame(people, columns=['Name', 'Designation'])
    people_df.to_excel('./names.xlsx', index=False)

    