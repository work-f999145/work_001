from bs4 import BeautifulSoup as BS
import numpy as np
import re
import pandas as pd

def details_of_the_complaint(page):
    """
        Сведения жалобы
    """
    soup = BS(page, 'html.parser')
    # Карточка со сведениями жалобы
    card = soup.find('div', string='Сведения жалобы')
    try:
        card = card.find_parent().find_parent()
    except AttributeError:
        out_text = np.NaN
    else:
        # Дата размещения жалобы
        card = card.find('div', string='Дата размещения жалобы')
        
        # Находим саму дату
        try:
            card = card.find_next_sibling('div', class_='common-text__value')
        except AttributeError:
            out_text = np.NaN
        else:
            try:
                out_text = card.get_text().strip()
            except AttributeError:
                out_text = np.NaN
    return out_text

def information_about_the_subject_of_control(page):
    """
        Информация о субъекте контроля:
            1.  Субъект контроля
            2.  Наименование организации
            3.  Почтовый адрес
            4.  Место нахождения
            5.  Номер телефона
    """
    
    soup = BS(page, 'html.parser')
    # Карточка с информацией
    card = soup.find('div', string='Информация о субъекте контроля')
    try:
        card = card.find_parent().find_parent()
    except AttributeError:
        out_tuple = (np.NaN, np.NaN, np.NaN, np.NaN, np.NaN) 
    else:
        # Субъект контроля
        subject = card.find('div', string='Субъект контроля')
        try:
            subject_out = subject.find_next_sibling('div', class_='common-text__value').get_text().strip()
        except AttributeError:
            subject_out = np.NaN
        
        # Наименование организации
        name_of_the_organization = card.find('div', string='Наименование организации')
        try:
            name_of_the_organization_out = name_of_the_organization.find_next_sibling('div', class_='common-text__value').get_text().strip()
        except AttributeError:
            name_of_the_organization_out = np.NaN
        
        # Почтовый адрес
        postal_address = card.find('div', string='Почтовый адрес')
        try:
            postal_address_out = postal_address.find_next_sibling('div', class_='common-text__value').get_text().strip()
        except AttributeError:
            postal_address_out = np.NaN
        
        # Место нахождения
        location = card.find('div', string='Место нахождения')
        try:
            location_out = location.find_next_sibling('div', class_='common-text__value').get_text().strip()
        except AttributeError:
            location_out = np.NaN
        
        # Номер телефона
        phone_number = card.find('div', string='Номер телефона')
        try:
            phone_number_out = phone_number.find_next_sibling('div', class_='common-text__value').get_text().strip()
        except AttributeError:
            phone_number_out = np.NaN
        
        out_tuple = (
            subject_out, 
            name_of_the_organization_out, 
            postal_address_out,
            location_out,
            phone_number_out
            )
    
    return out_tuple

def participant_data(page):
    """
        Данные участника контрактной системы в сфере закупок, подавшего жалобу
            Тип
            Фамилия, Имя, Отчество
            Дата постановки на учет в налоговом органе
            Место нахождения на территории РФ
                Номер телефона
                Место нахождения
                Адрес электронной почты
    """
    soup = BS(page, 'html.parser')
    # Карточка с информацией
    card = soup.find('div', string='Данные участника контрактной системы в сфере закупок, подавшего жалобу')
    
    try:
        card = card.find_parent().find_parent()
    except AttributeError:
        out_tuple = (np.NaN, np.NaN, np.NaN, np.NaN, np.NaN, np.NaN) 
    else:
        # Тип
        out_01 = card.find('div', string='Тип')
        try:
            out_01 = out_01.find_next_sibling('div', class_='common-text__value').get_text().strip()
        except AttributeError:
            out_01 = np.NaN
        
        # Фамилия, Имя, Отчество
        out_02 = card.find('div', string='Фамилия, Имя, Отчество')
        try:
            out_02 = out_02.find_next_sibling('div', class_='common-text__value').get_text().strip()
        except AttributeError:
            out_02 = np.NaN
            
        # Дата постановки на учет в налоговом органе
        out_03 = card.find('div', string='Дата постановки на учет в налоговом органе')
        try:
            out_03 = out_03.find_next_sibling('div', class_='common-text__value').get_text().strip()
        except AttributeError:
            out_03 = np.NaN

        # Номер телефона
        out_04 = card.find('div', string='Номер телефона')
        try:
            out_04 = out_04.find_next_sibling('div', class_='common-text__value').get_text().strip()
        except AttributeError:
            out_04 = np.NaN
        
        # Место нахождения
        out_05 = card.find('div', string='Место нахождения')
        try:
            out_05 = out_05.find_next_sibling('div', class_='common-text__value').get_text().strip()
        except AttributeError:
            out_05 = np.NaN
            
        # Адрес электронной почты
        out_06 = card.find('div', string='Адрес электронной почты')
        try:
            out_06 = out_06.find_next_sibling('div', class_='common-text__value').get_text().strip()
        except AttributeError:
            out_06 = np.NaN
        
        out_tuple = (out_01, out_02, out_03, out_04, out_05, out_06)
    
    return out_tuple

def content_of_the_complaint(page):
    """
        Содержание жалобы:
            Содержание жалобы
            Обжалуемые действия
    """

    soup = BS(page, 'html.parser')
    # Карточка с информацией
    card = soup.find('div', string=re.compile("Содержание жалобы"))

    try:
        card = card.find_parent().find_parent()
    except AttributeError:
        out_tuple = (np.NaN, np.NaN) 
    else:
        # Содержание жалобы
        out_01 = card.find('div', class_='common-text__title', string=re.compile("Содержание жалобы"))
        try:
            out_01 = out_01.find_next_sibling('div', class_='common-text__value').get_text().strip()
        except AttributeError:
            out_01 = np.NaN
        
        # Обжалуемые действия
        out_02 = card.find('div', string=re.compile("Обжалуемые действия"))
        try:
            out_02 = out_02.find_next_sibling('div', class_='common-text__value').get_text().strip()
        except AttributeError:
            out_02 = np.NaN
        
        out_tuple = (out_01, out_02)
    
    return out_tuple

def information_about_the_control_body(page):
    """
        Информация о контрольном органе в сфере закупок:
            Полное наименование
    """
    
    soup = BS(page, 'html.parser')
    # Карточка с информацией
    card = soup.find('div', string=re.compile("Информация о контрольном органе в сфере закупок"))

    try:
        card = card.find_parent().find_parent()
    except AttributeError:
        out_01 = np.NaN 
    else:
        # Содержание жалобы
        out_01 = card.find('div', class_='common-text__title', string=re.compile("Полное наименование"))
        try:
            out_01 = out_01.find_next_sibling('div', class_='common-text__value').get_text().strip()
        except AttributeError:
            out_01 = np.NaN
    
    return out_01



def purchase_information(page):
    """
        Сведения о закупке:
            Номер извещения
            Наименование закупки
            Дата размещения извещения об осуществлении закупки
    """
    soup = BS(page, 'html.parser')
        # Карточка с информацией
    card = soup.find('div', string='Сведения о закупке')

    try:
        card = card.find_parent().find_parent()
    except AttributeError:
        out_tuple = (np.NaN, np.NaN, np.NaN) 
    else:
        # Номер извещения
        out_01 = card.find('div', string='Номер извещения')
        try:
            out_01 = out_01.find_next_sibling('div', class_='common-text__value').find('a').get_text().strip()
        except AttributeError:
            out_01 = np.NaN
        
        # Наименование закупки
        out_02 = card.find('div', string='Наименование закупки')
        try:
            out_02 = out_02.find_next_sibling('div', class_='common-text__value').get_text().strip()
        except AttributeError:
            out_02 = np.NaN
            
        # Дата размещения извещения об осуществлении закупки
        out_03 = card.find('div', string=re.compile('Дата размещения извещения об осуществлении'))
        try:
            out_03 = out_03.find_next_sibling('div', class_='common-text__value').get_text().strip()
        except AttributeError:
            out_03 = np.NaN
        
        out_tuple = (out_01, out_02, out_03)

    return out_tuple





def information_about_the_acceptance_of_the_complaint_for_consideration(page):
    """
        Сведения о принятии жалобы к рассмотрению:
            Дата принятия жалобы к рассмотрению
            Дата и время рассмотрения жалобы
            Место рассмотрения жалобы
    """
    soup = BS(page, 'html.parser')
        # Карточка с информацией
    card = soup.find('div', string='Сведения о принятии жалобы к рассмотрению')

    try:
        card = card.find_parent().find_parent()
    except AttributeError:
        out_tuple = (np.NaN, np.NaN, np.NaN) 
    else:
        # Дата принятия жалобы к рассмотрению
        out_01 = card.find('div', string='Дата принятия жалобы к рассмотрению')
        try:
            out_01 = out_01.find_next_sibling('div', class_='common-text__value').get_text().strip()
        except AttributeError:
            out_01 = np.NaN
        
        # Дата и время рассмотрения жалобы
        out_02 = card.find('div', string='Дата и время рассмотрения жалобы')
        try:
            out_02 = out_02.find_next_sibling('div', class_='common-text__value').get_text().strip()
        except AttributeError:
            out_02 = np.NaN
            
        # Место рассмотрения жалобы
        out_03 = card.find('div', string=re.compile('Место рассмотрения жалобы'))
        try:
            out_03 = out_03.find_next_sibling('div', class_='common-text__value').get_text().strip()
        except AttributeError:
            out_03 = np.NaN
        
        out_tuple = (out_01, out_02, out_03)

    return out_tuple


def information_about_the_results_of_consideration_of_the_complaint(page):
    """
        Сведения о результатах рассмотрения жалобы:
            Результат рассмотрения жалобы
    """
    soup = BS(page, 'html.parser')
    # print(soup.prettify())
    # Карточка с информацией
    card = soup.find('div', string="Сведения о результатах рассмотрения жалобы")
    
    try:
        card = card.find_parent().find_parent()
    except AttributeError:
        out_01 = np.NaN 
    else:
        # Содержание жалобы
        out_01 = card.find('div', class_='common-text__title', string=re.compile("Результат рассмотрения жалобы"))
        try:
            out_01 = out_01.find_next_sibling('div', class_='common-text__value').find('div').get_text().strip()
        except AttributeError:
            out_01 = np.NaN
    
    return out_01

def parsing_information_from_the_site(page) -> pd.DataFrame:
    result_01_str = details_of_the_complaint(page)
    result_02_tuple = information_about_the_subject_of_control(page)
    result_03_tuple = participant_data(page)
    result_04_tuple = content_of_the_complaint(page)
    result_05_str = information_about_the_control_body(page)
    result_06_tuple = purchase_information(page)
    result_07_tuple = information_about_the_acceptance_of_the_complaint_for_consideration(page)
    result_08_str = information_about_the_results_of_consideration_of_the_complaint(page)
    
    named_01 = ['Дата размещения жалобы']
    
    named_02 = [
        'Субъект контроля',
        'Наименование организации',
        'Почтовый адрес',
        'Место нахождения субъекта контроля',
        'Номер телефона субъекта'
    ]
    
    named_03 = [
        'Тип',
        'Фамилия, Имя, Отчество',
        'Дата постановки на учет в налоговом органе',
        'Номер телефона заявителя',
        'Место нахождения',
        'Адрес электронной почты'
    ]
    
    named_04 = list(map(lambda x: x.strip(), """
        Содержание жалобы
        Обжалуемые действия

    """.strip().split('\n')))
    
    named_05 = ['Полное наименование']
    
    named_06 = list(map(lambda x: x.strip(), """
        Номер извещения
        Наименование закупки
        Дата размещения извещения об осуществлении закупки

    """.strip().split('\n')))
   
    named_07 = list(map(lambda x: x.strip(), """
        Дата принятия жалобы к рассмотрению
        Дата и время рассмотрения жалобы
        Место рассмотрения жалобы

    """.strip().split('\n')))
    
    named_08 = ['Результат рассмотрения жалобы']
    
    
    df1 = pd.DataFrame(data=[result_01_str], columns=named_01)
    df2 = pd.DataFrame(data=[result_02_tuple], columns=named_02)
    df3 = pd.DataFrame(data=[result_03_tuple], columns=named_03)
    df4 = pd.DataFrame(data=[result_04_tuple], columns=named_04)
    df5 = pd.DataFrame(data=[result_05_str], columns=named_05)
    df6 = pd.DataFrame(data=[result_06_tuple], columns=named_06)
    df7 = pd.DataFrame(data=[result_07_tuple], columns=named_07)
    df8 = pd.DataFrame(data=[result_08_str], columns=named_08)
    
    df = pd.concat([df1, df2, df3, df4, df5, df6, df7, df8], axis=1, sort=False)
    return df