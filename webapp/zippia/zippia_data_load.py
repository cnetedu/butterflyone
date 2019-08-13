from dataclasses import dataclass
from re import sub
from decimal import Decimal
import csv
import json
import bs4
import re
import os

def get_top_skills(soup):
    top_skills = soup.find('div', {'class': 'CareerTopSkills'})
    if top_skills:
        return [li.text.strip() for li in top_skills.find_all('li')]
    else:
        return []


def get_work_styles(soup):
    top_icons = soup.find('div', {'class': 'CareerTopDescribeIcons'})
    if top_icons:
        styles = [li.text for li in top_icons.find_all('li')]
        return [style for style in styles if 'Salary' not in style]
    return []


def get_salary(soup):
    salary_info = soup.find('p', {'class': 'salaryCMPInfo'})
    if salary_info:
        salary_str = salary_info.text.replace('$', '')
        value = Decimal(sub(r'[^\d.]', '', salary_str))
        return int(value.to_eng_string())
    return 0


def get_description(soup):
    moreDo = soup.find('div', {'class': 'ShowMorewhattheydoText'})
    if moreDo:
        p = moreDo.find('p')
        return p.text if p else ''
    return ''



def get_duties(soup):
    duties = []
    div = soup.find('div', {'class': 'ShowMorewhattheydoText'})
    if not div:
        return []
    ul = get_first_ul_after_strong_in_div(div, "Duties")
    if ul:
        for li in ul.find_all('li'):
            duties.append(li.text)
        return duties
    else:
        return []

def get_first_ul_after_strong_in_div(div, strong_text):
    found_strong_text = False
    for content in div.contents:
        if '<strong>{}'.format(strong_text) in repr(content):
            found_strong_text = True
        if found_strong_text is True and '<ul>' in repr(content):
            return content
    return None

def get_how_to_become(soup):
    more_become = soup.find('div', {"class": "ShowMorehowtobecomeText"})
    return more_become.find('p').text if more_become else ''


def get_paragraphs_after_strong_in_div(div, strong_text):
    found_strong_text = False
    paragraphs = []
    if not div:
        return ''
    for content in div.contents:
        if '<strong>' in repr(content) and '<strong>{}'.format(strong_text) not in repr(content):
            found_strong_text = False
        if '<strong>{}'.format(strong_text) in repr(content):
            found_strong_text = True
        if found_strong_text is True and '<p>' in repr(content):
            paragraphs.append(content.text)
    return '\n'.join(paragraphs)


def get_div_for_becoming(div):
    return div.find('div', {"class": "ShowMorehowtobecomeText"})


def get_qualities(div):
    ems = [em.text for em in div.find_all('em')]
    to_remove = []
    for idx, quality in enumerate(ems):
        if quality == 'skills.' or quality == 'skills' and idx > 0:
            to_remove.append(idx)

    for tf in to_remove:
        ems[tf-1] = "{} skills".format(ems[tf-1])
    for rm in to_remove:
        del ems[rm]
    return [re.sub(r'\.$', '', em) for em in ems]


def get_avg_length_of_employment(soup, title):
    divs = soup.find_all('div', {'class': 'percentageItemListTextRow'})
    for div in divs:
        if 'years' not in repr(div):
            continue
        if title in div.text:
            return float(div.find('span').text.replace(' years', '').strip())
    return 0.0


def get_majors(soup):
    return get_container_with_percentages_by_title(soup, 'Majors')


acceptable_degrees = ['Bachelors', 'Other', 'Associate', 'Masters', 'Certificate', 'Diploma', 'Doctorate', 'License']


def get_degrees(soup):
    tds = soup.find_all('td', {'class': 'educationDegrees'})
    degrees = []
    for td in tds:
        for acceptable in acceptable_degrees:
            if acceptable in td.text:
                degrees.append((td.find('p').text, td.find('span').text.replace('%', '')))

    return degrees

def get_container_with_percentages_by_title(soup, title):
    trs = soup.find_all('tr', {'class': 'percentageContainer'})
    found_title = False
    results = dict()
    for tr in trs:
        if 'companyPageSub' in repr(tr):
            found_title = False
            if title in tr.text:
                found_title = True

        if found_title and 'percentageItemListName' in repr(tr):
            tr_name = tr.find('p', {'class': 'percentageItemListName'})
            if tr_name:
                name = tr_name.text
            tr_span = tr.find('span')
            if tr_span:
                percentage = tr_span.text
            if tr_name and tr_span:
                results[name] = percentage
    return results



def get_skills(soup):
    skill_graph_data = soup.find('div', {"class": "skillGraphData"})
    if skill_graph_data:
        return [li.text.strip() for li in skill_graph_data.find_all('li')[:3]]
    return []


def get_other_skills(div):
    return [t.text for t in div.find_all('text')]


def get_employers(soup):
    section = soup.find('section', {'id': 'employers'})
    if section:
        return [li.text.strip() for li in section.find_all('li')]
    return []


def get_career_path(soup):
    rows = soup.find_all('section', {"class", "MapCarrerRow"})
    return_rows = []
    if len(rows) == 0:
        return []
    else:
        for row in rows:
            result_row = [r.text for r in row.find_all('span')[:-2]]
            if result_row:
                return_rows.append(result_row)
        return return_rows


def create_job_object(html_contents, industry_lookup):
    soup = bs4.BeautifulSoup(html_contents, 'html.parser')
    title = soup.find('h2', {'class': 'cmp-section-title'}).text.replace('Working As A ', '')
    top_skills = json.dumps(get_top_skills(soup))
    work_styles = json.dumps(get_work_styles(soup))
    avg_salary = get_salary(soup)
    description = get_description(soup)
    duties = json.dumps(get_duties(soup))
    how_to_become = get_how_to_become(soup)

    div = get_div_for_becoming(soup)
    education = get_paragraphs_after_strong_in_div(div, 'Education')
    licenses = get_paragraphs_after_strong_in_div(div, 'Licenses')
    advancement = get_paragraphs_after_strong_in_div(div, 'Advancement')
    if div:
        qualities = json.dumps(get_qualities(div))
    else:
        qualities  = ''
    avg_length_of_employment_yr = get_avg_length_of_employment(soup, title)
    career_path = json.dumps(get_career_path(soup))
    majors = json.dumps(get_majors(soup))
    degrees = json.dumps(get_degrees(soup))
    skills = json.dumps(get_skills(soup))
    other_skills = json.dumps(get_other_skills(soup))
    top_employers = json.dumps(get_employers(soup))
    return Job(title=title, top_skills=top_skills, avg_salary=avg_salary,description=description, duties=duties,
               work_styles=work_styles, industry=industry_lookup.get(title, 'Unknown'),
               how_to_become=how_to_become, education=education, licenses=licenses, advancement=advancement,
               qualities=qualities, avg_length_of_employment_yr=avg_length_of_employment_yr, majors=majors,
               degrees=degrees, skills=skills, other_skills=other_skills, top_employers=top_employers,
               career_path=career_path)

def write_to_job_csv(job_object, writer):
    row_attrs = []
    for attr in ['title', 'top_skills', 'work_styles', 'avg_salary', 'description', 'duties',
                             'how_to_become', 'education', 'licenses', 'qualities', 'advancement',
                             'avg_length_of_employment_yr', 'majors', 'degrees', 'skills', 'other_skills',
                             'top_employers', 'career_path']:
        row_attrs.append(getattr(job_object, attr, ''))
    writer.writerow(row_attrs)

import queue
from threading import Thread
def do_stuff(q, i, industries):
    with open('jobs_csv_{}.csv'.format(i), 'w') as w:
        csv_writer = csv.writer(w, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow(['title', 'top_skills', 'work_styles', 'avg_salary', 'description', 'duties',
                             'how_to_become', 'education', 'licenses', 'qualities', 'advancement',
                             'avg_length_of_employment_yr', 'majors', 'degrees', 'skills', 'other_skills',
                             'top_employers', 'career_path'])
        count = 0
        while True:
            file_path = q.get()
            with open(file_path) as fn:
                try:
                    job_object = create_job_object(fn.read(), industries)
                    write_to_job_csv(job_object, csv_writer)
                except Exception as ex:
                    print("The following file had an issue: {}. Ex: {}".format(file_path, ex))
                count += 1
            if count % 100 == 0:
                print('Thread {} up to {}'.format(i, count))
            q.task_done()
#     title = soup.find('h2', {'class': 'cmp-section-title'}).text.replace('Working As A ', '')



def create_jobs_csvs(industries):
    fqueue = queue.Queue()
    for i in range(10):
        worker = Thread(target=do_stuff, args=(fqueue,i,industries))
        worker.setDaemon(True)
        worker.start()

    for f in os.listdir('/Users/george/butterflyone/webapp/jobs'):
        fqueue.put('/Users/george/butterflyone/webapp/jobs/' + f)
    fqueue.join()

@dataclass
class Job:
    title: str
    top_skills: str # top
    work_styles: str # top icons
    avg_salary: int
    industry: str
    description: str # top paragraph of what do
    duties: str # list of duties in paragraph
    how_to_become: str # top paragraph of how to
    education: str # section
    licenses: str # section
    qualities: str # section in Important Qualities
    advancement: str #section
    avg_length_of_employment_yr: float
    majors: str # dictionary of name to percentage
    degrees: str # dictionary of
    skills: str # List
    other_skills: str # List
    top_employers: str # List
    career_path: str # json of path


def get_major_jobs(soup):
    title_list = soup.find('div', {'class': 'top-title-list'})
    if title_list:
        return [li.text for li in title_list.find_all('li')]
    else:
        return []


def get_career_path_for_major(soup):
    rows = soup.find_all('section', {"class", "MapCarrerRow"})
    return_rows = []
    return_years = []
    if len(rows) == 0:
        return [], []
    else:
        for row in rows:
            result_row = [r.text for r in row.find_all('span')[:-2]]
            end_year = 0
            if result_row:
                end_year = row.find('div', {'class': 'elementTimelineLastYears'}).text.split(' ')[0]

                return_years.append("{} -- {} -- {}".format(result_row[0], result_row[-1], end_year))
                return_rows.append(result_row)
        return return_rows, return_years


def create_major_object(html_contents):
    soup = bs4.BeautifulSoup(html_contents, 'html.parser')
    name = soup.find('h2', {'class': 'cmp-section-title'}).text.replace(' Career Paths', '')

    career_path_dict, return_years = get_career_path_for_major(soup)
    best_job_1= ""
    best_job_2=""
    best_job_3=""
    career_paths = json.dumps(career_path_dict)
    job_duration = json.dumps(return_years)

    if len(career_path_dict) > 0:
        best_job_1 = career_path_dict[0]

    if len(career_path_dict) > 1:
        best_job_2 = career_path_dict[1]

    if len(career_path_dict) > 2:
        best_job_3 = career_path_dict[2]

    return Major(name=name, career_paths=career_paths, job_duration=job_duration)


class Node(object):
    def __init__(self, name, is_child):
        self.name = name
        self.next = []
        self.is_child = is_child

    def __repr__(self):
        return self.name


def create_major_tree(career_dict):
    lookup = dict()
    for career_path in career_dict:
        child_name = career_path[0]
        child_node = lookup.get(child_name, Node(child_name, True))
        child_node.is_child = True
        lookup[child_name] = child_node

        for i in range(len(career_path)-1, 0, -1):
            curr_job = career_path[i]
            next_job = career_path[i-1]
            curr_node = lookup.get(curr_job, Node(curr_job, False))
            next_node = lookup.get(next_job, Node(next_job, next_job == child_name))
            curr_node.next.append(next_node)
            lookup[curr_job] = curr_node
            lookup[next_job] = next_node
    return lookup


def find_children_in_tree(job_name, career_dict):
    children = []
    to_lookup = [career_dict.get(job_name)]
    seen = set()
    while to_lookup:
        curr = to_lookup.pop()
        if curr.name in seen:
            continue
        for n in curr.next:
            to_lookup.insert(0, career_dict.get(n.name))
        if curr.is_child:
            children.append(curr.name)
        seen.add(curr.name)
    return list(set(children))


def create_major_lookup_object(html_contents):
    soup = bs4.BeautifulSoup(html_contents, 'html.parser')
    name = soup.find('h2', {'class': 'cmp-section-title'}).text.replace(' Career Paths', '')

    career_path_dict, _ = get_career_path_for_major(soup)

    major_lookups = []

    career_tree = create_major_tree(career_path_dict)

    for career_path in career_path_dict:
        if not career_path:
            pass

        final_job = career_path[-1]

        for job in career_path:
            entry_levels = find_children_in_tree(job, career_tree)
            entry_levels = list(filter(lambda entry_level: entry_level not in career_path[1:], entry_levels))

            major_lookups.append(
                    MajorLookup(name=name,
                                career_name=job,
                                entry_levels=list(entry_levels),
                                final=job == final_job,
                                path=json.dumps(career_path)))

    return major_lookups


def create_majors_csv():
    with open('majors.csv', 'w', encoding='utf8') as w:
        csv_writer = csv.writer(w, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow(['name', 'career_name', 'entry_levels', 'final', 'path', ''])
        for f in os.listdir('/Users/george/butterflyone/webapp/majors'):
            with open('/Users/george/butterflyone/webapp/majors/' + f) as fn:
                major_lookups = create_major_lookup_object(fn.read())
                for lookup in major_lookups:
                    csv_writer.writerow([lookup.name, lookup.career_name, lookup.entry_levels, lookup.final, lookup.path])


@dataclass
class MajorLookup:
    name: str
    career_name: str
    entry_levels: str
    final: bool
    path: str


def create_majors_lookup_csv():
    with open('majors_lookup.csv', 'w', encoding='utf8') as w:
        csv_writer = csv.writer(w, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow(['name', 'career_paths', 'job_duration'])
        for f in os.listdir('/Users/george/butterflyone/webapp/majors'):
            with open('/Users/george/butterflyone/webapp/majors/' + f) as fn:
                major = create_major_object(fn.read())
                csv_writer.writerow([major.name, major.career_paths, major.job_duration])

#### building industries dictionary
def parse_industry_file(file_path, industries):
    with open(file_path) as f:
        header = f.readline()
        try:
            industry = header.split('Industry:')[1].split(' Link:')[0]
        except:
            import pdb; pdb.set_trace()
        for line in f:
            if '-jobs' in line:
                job_name = ','.join(line.split(',')[:-1])
                industries[job_name] = industry


def make_industries():
    industries = dict()
    for f in os.listdir('/Users/george/butterflyone/webapp/industries'):
        if 'map' not in f:
            parse_industry_file('/Users/george/butterflyone/webapp/industries/' + f, industries)
    return industries


@dataclass
class Major:
    name: str
    career_paths: str # list of all best jobs
    job_duration: str # json of path
