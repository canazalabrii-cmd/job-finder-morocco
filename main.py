import requests
from bs4 import BeautifulSoup
import time
from telegram import Bot
import os

# إعدادات تلغرام
TELEGRAM_TOKEN = os.environ.get('8289814129:AAGhJL_DjLl104OwK1RsxZ90DiNP6hynqGc')
CHAT_ID = os.environ.get('198842533')

# الكلمات المفتاحية للبحث
KEYWORDS = ['محاسب', 'comptable', 'accountant', 'finance', ' comptabilité']
LOCATIONS = ['الرباط', 'تمارة', 'Rabat', 'Temara']

def send_telegram_message(message):
    """إرسال رسالة على تلغرام"""
    try:
        bot = Bot(token=TELEGRAM_TOKEN)
        bot.send_message(chat_id=CHAT_ID, text=message)
    except Exception as e:
        print(f"خطأ في إرسال الرسالة: {e}")

def search_indeed():
    """البحث في indeed.ma"""
    jobs = []
    try:
        url = "https://ma.indeed.com/jobs?q=accountant&l=Rabat"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        job_cards = soup.find_all('div', class_='job_seen_beacon')
        
        for card in job_cards:
            title_elem = card.find('h2', class_='jobTitle')
            company_elem = card.find('span', class_='companyName')
            location_elem = card.find('div', class_='companyLocation')
            
            if title_elem and company_elem:
                title = title_elem.get_text().strip()
                company = company_elem.get_text().strip()
                location = location_elem.get_text().strip() if location_elem else "غير محدد"
                
                # التحقق من الكلمات المفتاحية والمواقع
                if any(keyword.lower() in title.lower() for keyword in KEYWORDS) or \
                   any(keyword.lower() in company.lower() for keyword in KEYWORDS):
                    if any(loc.lower() in location.lower() for loc in LOCATIONS):
                        job_link = "https://ma.indeed.com" + title_elem.find('a')['href'] if title_elem.find('a') else ""
                        job_info = f"💼 Indeed - وظيفة جديدة:\nعنوان: {title}\nالشركة: {company}\nالموقع: {location}\nالرابط: {job_link}"
                        jobs.append(job_info)
    except Exception as e:
        print(f"خطأ في indeed: {e}")
    
    return jobs

def search_emploi_ma():
    """البحث في emploi.ma"""
    jobs = []
    try:
        url = "https://www.emploi.ma/recherche-jobs-maroc/accountant"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        job_listings = soup.find_all('div', class_='job-item')
        
        for job in job_listings:
            title_elem = job.find('h3')
            company_elem = job.find('div', class_='company-name')
            location_elem = job.find('div', class_='job-location')
            
            if title_elem and company_elem:
                title = title_elem.get_text().strip()
                company = company_elem.get_text().strip()
                location = location_elem.get_text().strip() if location_elem else "غير محدد"
                
                # التحقق من الكلمات المفتاحية والمواقع
                if any(keyword.lower() in title.lower() for keyword in KEYWORDS) or \
                   any(keyword.lower() in company.lower() for keyword in KEYWORDS):
                    if any(loc.lower() in location.lower() for loc in LOCATIONS):
                        job_link_elem = title_elem.find('a')
                        job_link = "https://www.emploi.ma" + job_link_elem['href'] if job_link_elem else ""
                        job_info = f"💼 Emploi.ma - وظيفة جديدة:\nعنوان: {title}\nالشركة: {company}\nالموقع: {location}\nالرابط: {job_link}"
                        jobs.append(job_info)
    except Exception as e:
        print(f"خطأ في emploi.ma: {e}")
    
    return jobs

def main():
    """الدالة الرئيسية"""
    print("جاري البحث عن وظائف...")
    
    # البحث في المواقع
    indeed_jobs = search_indeed()
    emploi_jobs = search_emploi_ma()
    
    all_jobs = indeed_jobs + emploi_jobs
    
    if all_jobs:
        message = f"📊 تم العثور على {len(all_jobs)} وظيفة جديدة!\n\n" + "\n\n".join(all_jobs)
        send_telegram_message(message)
        print(f"تم إرسال {len(all_jobs)} وظيفة")
    else:
        print("لا توجد وظائف جديدة")

if __name__ == "__main__":
    main()
