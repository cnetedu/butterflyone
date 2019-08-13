import zippia.zippia_data_load
import json
import os


def test_zippia_job_load_finance_analyst():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    industries_lookup = {"Senior Finance Analyst": "Finance Industry"}

    with open('{}/senior-finance-analyst.html'.format(current_dir)) as test_finance_analyst_file:
        job = zippia.zippia_data_load.create_job_object(test_finance_analyst_file.read(), industries_lookup)
        assert job.title == 'Senior Finance Analyst', "title is wrong"

        expected_top_skills = [
            "Analyzing Data or Information", "Getting Information", "Interacting With Computers",
            "Processing Information", "Communicating with Supervisors, Peers, or Subordinates"]

        for skill in expected_top_skills:
            assert skill in job.top_skills, "Skill '{}' should have been in top skills".format(skill)

        expected_work_styles = ["Deal with People", "Mostly Sitting", "Repetitive"]
        for work_style in expected_work_styles:
            assert work_style in job.work_styles

        expected_avg_salary = 119190
        assert job.avg_salary == expected_avg_salary, 'Salary was wrong'

        expected_do = "Financial analysts do x."
        assert expected_do == job.description, "Financial Analysts description was wrong."

        expected_duties = '["Assess the strength of the management team", "Prepare written reports"]'
        assert expected_duties == job.duties


        expected_how_to_become = "Financial analysts typically must have a bachelor’s degree."
        assert expected_how_to_become == job.how_to_become, "How to become is wrong."

        expected_education = "Most positions require a bachelor's degree."
        assert expected_education == job.education, "Education is wrong"

        expected_licenses = "FINRA\nCFA"
        assert expected_licenses == job.licenses

        expected_qualities = ["Analytical skills", "Communication skills", "Computer skills", "Mathematical skills"]
        for quality in expected_qualities:
            assert quality in job.qualities

        expected_advancement = "Financial analysts typically start by specializing in a specific investment field."
        assert expected_advancement == job.advancement, "Advancement is wrong"

        expected_length_of_employment = 4.0
        assert expected_length_of_employment == job.avg_length_of_employment_yr

        assert job.industry == "Finance Industry"

        expected_career_path = '[["Business Manager", "Payroll Administrator", "Assistant Controller", ' \
                               '"Assistant Corporate Controller"], ["Assistant Vice President", ' \
                               '"Finance Consultant", "Finance Manager", "Business Manager-Finance Manager"], ' \
                               '["Finance Manager", "Controller", "Controller, Vice President"], ' \
                               '["Plant Controller", "Finance Manager", "Controller", "Controller/Business Manager"], ' \
                               '["Plant Controller", "Division Controller", "Controller", ' \
                               '"Controller/Director Of Finance"], ["Finance Supervisor", "Finance Manager", ' \
                               '"Controller", "Controller/Finance Manager"], ["Controller", "Accounting Consultant", ' \
                               '"Accounting Manager", "Corporate Accounting Manager"], ["Senior Consultant", ' \
                               '"Senior Manager", "Controller", "Director Of Accounting & Finance"], ' \
                               '["Operations Manager", "Bookkeeper", "Accounting Manager", "Division Controller"], ' \
                               '["Accounting Consultant", "Accounting Manager", "Assistant Controller", ' \
                               '"Divisional Controller"], ["Operations Manager", "Analyst", "Finance Analyst", ' \
                               '"Finance Planning Manager"], ["Cost Accounting Manager", "Plant Controller", ' \
                               '"Controller", "Group Controller"], ["Manager Finance Planning And Analysis", ' \
                               '"Controller", "Interim Controller"], ["Manager-Finance Systems"], ' \
                               '["Assistant Vice President", "Office Manager", "Accounting Manager", ' \
                               '"Manager/Finance Accounting"], ["Finance Manager", "Business Manager", ' \
                               '"Controller", "Regional Controller"], ["Business Manager", "Service Manager", ' \
                               '"Finance Manager", "Regional Finance Manager"], ["Controller", ' \
                               '"Accountant-Contractor", "Senior Accountant", "Reporting Manager"], ' \
                               '["Cost Accounting Manager", "Accounting Manager", "Senior Accounting Manager"], ' \
                               '["Reporting Manager", "Assistant Controller", "Plant Controller", "Unit Controller"]]'

        assert job.career_path == expected_career_path
        expected_majors = {"Business": "31.6%", "Finance": "28.0%", "Accounting": "24.9%"}
        loaded_major_dict = json.loads(job.majors)

        for major in expected_majors:
            assert expected_majors[major] == loaded_major_dict[major]
        expected_skills = ['Financial Statements', 'Variance Analysis', 'A/P']
        for skill in expected_skills:
            assert skill in job.skills
        expected_other_skills = ['Financial Statements', 'Variance Analysis', 'A/P', 'Assets', 'Business Units',
                                 'External Auditors', 'Balance Sheet', 'Journal Entries', 'General Ledger Accounts',
                                 'Financial Models', 'Financial Performance', 'Cost Savings', 'Financial Support',
                                 'Gaap', 'SOX', 'Account Reconciliations', 'Special Projects', 'Loss', 'Payroll',
                                 'ERP', 'Capital Projects', 'Key Performance Indicators', 'Executive Management',
                                 'Monthly Basis', 'Process Improvement']
        for skill in expected_other_skills:
            assert skill in job.other_skills

        expected_employers = ['Amazon', 'Bank of America', 'HP', 'General Motors', 'Intel', 'The Walt Disney Company',
                              'Lockheed Martin', 'IBM', 'Cummins', 'American Airlines']
        for employer in expected_employers:
            assert employer in job.top_employers
