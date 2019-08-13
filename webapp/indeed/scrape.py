from indeed import IndeedClient
from dataclasses import dataclass
import csv
import time

client = IndeedClient(publisher=8924341972846274)

@dataclass
class JobListing:
    jobTitle: str
    company: str
    city: str
    state: str
    country: str
    source: str
    url: str
    snippet: str
    date: str
    jobkey: str
    indeedApply: bool


def get_params(q, start):
    return {'q': q,
        'l' : "new york city",
        'userip' : "1.2.3.4",
        'start': start,
        'useragent' : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2)",
        'jt': 'internship',
        'limit': 20
        }


def search(q):
    start = 0
    totalResults = 100
    seen = set()

    while start < 1000:
        results = client.search(**get_params('internship', start))
        totalResults = results['totalResults']
        start = results['start'] + 20
        for job_dict in results.get('results', []):
            jobkey=job_dict['jobkey']

            if jobkey in seen:
                continue

            seen.add(jobkey)
            yield JobListing(
                jobTitle=job_dict['jobtitle'],
                company=job_dict['company'],
                city=job_dict['city'],
                state=job_dict['state'],
                country=job_dict['country'],
                source=job_dict['source'],
                url=job_dict['url'],
                snippet=job_dict['snippet'],
                date=job_dict['date'],
                jobkey=jobkey,
                indeedApply=job_dict['indeedApply']
            )

        print("Count: {}. Start: {}".format(len(seen), start))
        time.sleep(0.5)


def write_job_to_csv():
    with open('indeed.csv', 'w', encoding='utf8') as w:
        csv_writer = csv.writer(w, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow(['jobkey', 'jobTitle', 'company', 'city', 'state', 'country', 'source', 'url', 'snippet', 'date', 'indeedApply'])
        for job_listing in search('internship'):
            csv_writer.writerow([job_listing.jobkey, job_listing.jobTitle, job_listing.company, job_listing.city,
                                 job_listing.state, job_listing.country, job_listing.source, job_listing.url, job_listing.snippet,
                                 job_listing.date, job_listing.indeedApply])
