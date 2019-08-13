from dataclasses import dataclass
import datetime
import requests
import time
import bs4
import string


@dataclass
class Job:
    name: str
    description: str
    how_to_become_an_application_engineer: str
    # top_skills: List
    discipline: str
    avg_length_of_employment_in_years: float

@dataclass
class Industry:
    name: str
    link: str

@dataclass
class JobLink:
    name: str
    link: str


@dataclass
class Major:
    name: str
    link: str


def parse_career_details(soup):
    discipline = soup.find('div', {'class': 'CareerMaPTitleText'}).text.strip()


def parse_career_path(url):
    page = requests.get(url)
    soup = bs4.BeautifulSoup(page.content, 'html.parser')
    return parse_user_info(soup), parse_education(soup), parse_experience(soup)


def scrape_industries(driver):
    soup = bs4.BeautifulSoup(driver.page_source, 'html.parser')
    div = soup.find('section', {'class': 'industries-sec'})
    industries = []

    for li in div.find_all('li'):
        name = li.find('span', {'class': 'industry-title'}).text
        link = driver.current_url + li.find('a').attrs['href'][1:]
        industries.append(Industry(name, link=link))
    return industries


def parse_job_links(driver):
    soup = bs4.BeautifulSoup(driver.page_source, 'html.parser')
    job_links = []
    for a in soup.find_all('a', {'class': 'list-link'}):
        job_links.append(JobLink(name=a.text, link=a.attrs['href']))
    return job_links


def login(chromedriver):
    chromedriver.get('https://www.linkedin.com/uas/login')
    chromedriver.find_element_by_id('username').send_keys('george.m.sequeira@gmail.com')
    chromedriver.find_element_by_id('password').send_keys('nEcmultisync%0')
    chromedriver.find_element(By.CLASS_NAME, 'btn__primary--large').click()


def industry_to_careers():
    # need to have chrome in thepath
    chromedriver = webdriver.Chrome()
    chromedriver.get('https://www.zippia.com/')
    list_of_industries = scrape_industries(chromedriver)
    # store industries and where to find them.
    with open('/Users/george/butterflyone/webapp/industries/map.txt', 'w') as w:
        for industry in list_of_industries:
            w.write('{},{}\n'.format(industry.name, industry.link))

    for industry in list_of_industries:
        job_links = []
        for letter in string.ascii_lowercase:
            chromedriver.get(industry.link + letter)
            letter_links = parse_job_links(chromedriver)
            job_links.extend(letter_links)
        code_industry = hash(industry.name + industry.link)
        with open('/Users/george/butterflyone/webapp/industries/{}.txt'.format(code_industry), 'w') as industry_out:
            industry_out.write('Industry:{} Link:{}\n\n'.format(industry.name, industry.link))
            for job_link in job_links:
                industry_out.write('{},{}\n'.format(job_link.name, job_link.link))
        time.sleep(0.2)


def scrape_jobs(driver):
    soup = bs4.BeautifulSoup(driver.page_source, 'html.parser')
    major_link = []
    for li in soup.find('ul', {'class': 'site-nav'}).find_all('li'):
        a = li.find('a')
        major_link.append(Major(name=a.text, link=a.attrs['href']))
    return job_links


def scrape_majors(driver):
    soup = bs4.BeautifulSoup(driver.page_source, 'html.parser')
    major_link = []
    for li in soup.find('div', {'id': 'allMajors'}).find('ul', {'class': 'site-nav'}).find_all('li'):
        a = li.find('a')
        major_link.append(Major(name=a.text, link=a.attrs['href']))
    return major_link


def major_dumps():
    chromedriver = webdriver.Chrome()
    chromedriver.get('https://www.zippia.com/majors')
    list_of_majors = scrape_majors(chromedriver)
    for major in list_of_majors:
        chromedriver.get(major.link)
        major_lower_spaced = major.name.replace(' ', '-').replace(',', '_').replace('/', '_').lower()
        with open('/Users/george/butterflyone/webapp/majors/{}.html'.format(major_lower_spaced), 'w') as wout:
            wout.write("Major: {}, MajorLink {}\n\n\n\n".format(major.name, major.link))
            wout.write(chromedriver.page_source)
        time.sleep(0.3)


def make_file_name(job_name):
    name = job_name.replace(' ', '-').replace(',', '_').replace('/', '_').replace("'", '').lower()
    return '/Users/george/butterflyone/webapp/jobs/{}.html'.format(name)


def job_dumps():
    count = 0
    done = set()
    for f in os.listdir('/Users/george/butterflyone/webapp/industries'):
        with open('/Users/george/butterflyone/webapp/industries/' + f) as job_file:
            for line in job_file:
                count += 1
                if 'jobs' in line:
                    split_line = line.split(',')
                    name = ', '.join(split_line[:-1])
                    url = split_line[-1].strip()
                    fn = make_file_name(name)
                    if os.path.exists(fn):
                        # print('Skipping: %s' % fn)
                        continue

                    try:
                        response = requests.get(url)
                    except Exception as e:
                        print("Had issue: %s -- %s" % (name,url))
                        print(e)
                        continue


                    if response.status_code == 200:
                        with open(fn, 'w') as wout:
                            wout.write(str(response.content, 'utf-8'))
                    else:
                        print("Uh oh. Issue with: %s" % url)
                if count % 100 == 0:
                    print("Done another 100: %s, %s" % (count, datetime.datetime.utcnow()))

        print("done with file: %s" % f)


def grab_extras_that_dont_exist():
    jobs_in_htmls = set()
    for f in os.listdir('/Users/george/butterflyone/webapp/jobs'):
        with open('/Users/george/butterflyone/webapp/jobs/' + f) as job_file:
            soup = bs4.BeautifulSoup(job_file.read())
            for a in soup.find_all('a', {'class': 'elementTimeline'}):
                jobs_in_htmls.add(a.find('span').text)
    return jobs_in_htmls


def grab_extra_jobs_that_dont_exist(list_of_job_names):
    for job_name in list_of_job_names:
        normal_name = job_name.replace(',', '-').replace(' ', '-').replace("'", '-').lower()
        url = "https://www.zippia.com/{}-jobs/".format(normal_name)

        fn = make_file_name(job_name)
        if os.path.exists(fn):
            print('Skipping: %s' % fn)
            continue

        try:
            response = requests.get(url)
        except Exception as e:
            print("Had issue: %s -- %s" % (name, url))
            print(e)
            continue

        if response.status_code == 200:
            with open(fn, 'w') as wout:
                wout.write(str(response.content, 'utf-8'))
        else:
            print("Uh oh. Issue with: %s" % url)