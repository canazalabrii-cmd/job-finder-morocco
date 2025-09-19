import requests
from bs4 import BeautifulSoup
from telegram import Bot
import os

# ---------------- إعدادات تلغرام ----------------
# إما تستعمل متغيرات بيئية (Secrets) أو تكتبهم مباشرة هنا
TELEGRAM_TOKEN = os.environ.get('8289814129:AAGhJL_DjLl104OwK1RsxZ90DiNP6hynqGc') or "ضع_هنا_التوكن"
CHAT_ID = os.environ.get('198842533') or "ضع_هنا_CHAT_ID"

# الكلمات المفتاحية والمواقع للبحث
KEYWORDS = ['محاسب', 'comptable', 'accountant', 'finance']
LOCATIONS = ['الرباط', 'تمارة', 'Rabat', 'Temara']

# ---------------- إرسال رسالة لتلغرام ----------------
def send_telegram_message(message: str):
    try:
        bot = Bot(token=TELEGRAM_TOKEN)
        bot.send_message(chat_id=CHAT_ID, text=message)
        print("✅ تم إرسال الرسالة إلى تلغرام")
    except Exception as e:
        print(f"⚠ خطأ في إرسال الرسالة: {e}")

# ---------------- البحث في Indeed ----------------
def search_indeed():
    jobs = []
    try:
        url = "https://ma.indeed.com/jobs?q=accountant&l=Rabat"
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        job_cards = soup.find_all('div', class_='job_seen_beacon')
        for card in job_cards:
            title_elem = card.find('h2', class_='jobTitle')
            company_elem = card.find('span', class_='companyName')
            location_elem = card.find('div', class_='companyLocation')
            
            if title_elem and company_elem:
                title = title_elem.get_text(strip=True)
                company = company_elem.get_text(strip=True)
                location = location_elem.get_text(strip=True) if location_elem else "غير محدد"
                
                # تحقق من الكلمات المفتاحية والمواقع
                keyword_match = any(k.lower() in title.lower() or k.lower() in company.lower() for k in KEYWORDS)
                location_match = any(l.lower() in location.lower() for l in LOCATIONS)
                
                if keyword_match and location_match:
                    link_elem = title_elem.find('a')
                    job_link = "https://ma.indeed.com" + link_elem['href'] if link_elem else ""
                    jobs.append(f"💼 Indeed - وظيفة جديدة:\nعنوان: {title}\nالشركة: {company}\nالموقع: {location}\nالرابط: {job_link}")
    except Exception as e:
        print(f"⚠ خطأ في indeed: {e}")
    return jobs

# ---------------- البحث في Emploi.ma ----------------
def search_emploi_ma():
    jobs = []
    try:
        url = "https://www.emploi.ma/recherche-jobs-maroc/accountant"
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        job_listings = soup.find_all('div', class_='job-item')
        for job in job_listings:
            title_elem = job.find('h3')
            company_elem = job.find('div', class_='company-name')
            location_elem = job.find('div', class_='job-location')
            
            if title_elem and company_elem:
                title = title_elem.get_text(strip=True)
                company = company_elem.get_text(strip=True)
                location = location_elem.get_text(strip=True) if location_elem else "غير محدد"
                
                keyword_match = any(k.lower() in title.lower() or k.lower() in company.lower() for k in KEYWORDS)
                location_match = any(l.lower() in location.lower() for l in LOCATIONS)
                
                if keyword_match and location_match:
                    link_elem = title_elem.find('a')
                    job_link = "https://www.emploi.ma" + link_elem['href'] if link_elem else ""
                    jobs.append(f"💼 Emploi.ma - وظيفة جديدة:\nعنوان: {title}\nالشركة: {company}\nالموقع: {location}\nالرابط: {job_link}")
    except Exception as e:
        print(f"⚠ خطأ في emploi.ma: {e}")
    return jobs

# ---------------- الدالة الرئيسية ----------------
def main():
    print("🔍 جاري البحث عن وظائف...")
    indeed_jobs = search_indeed()
    emploi_jobs = search_emploi_ma()
    
    all_jobs = indeed_jobs + emploi_jobs
    if all_jobs:
        message = f"📊 تم العثور على {len(all_jobs)} وظيفة جديدة!\n\n" + "\n\n".join(all_jobs)
        send_telegram_message(message)
        print(f"✅ تم إرسال {len(all_jobs)} وظيفة")
    else:
        print("ℹ لا توجد وظائف جديدة حالياً")

if _name_ == "_main_":
    main()
