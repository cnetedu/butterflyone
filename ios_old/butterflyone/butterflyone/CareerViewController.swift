//
//  CareerViewController.swift
//  butterflyone
//
//  Created by George Sequeira on 7/18/19.
//  Copyright © 2019 George Sequeira. All rights reserved.
//

import UIKit
import Alamofire
import SwiftyJSON

class CareerViewController: UIViewController {
    var majors: [String]?
    var locations: [String]?

    @IBOutlet weak var jobsView: UITextView!
    @IBOutlet weak var jobTitleView: UITextView!

    override func viewDidLoad() {
        super.viewDidLoad()
        // majors=Psychology
        let defaults = UserDefaults.standard
        self.majors = defaults.object(forKey: "majors") as? [String]
        self.locations = defaults.object(forKey: "locations") as? [String]

        jobTitleView.text = "Loading job titles..."
        jobsView.text = "Loadding job postings..."
        // Do any additional setup after loading the view.
        if majors != nil {
            retrieveJobTitles(majors!)
        }
    }

    func retrieveJobTitles(_ majors: [String]) {
        var url = "https://moonlit-cistern-243518.appspot.com/jobs_by_majors?"
        for major in majors {
            url = url + "majors=\(major)&"
        }

        Alamofire.request(url, method: .get)
            .responseJSON{response in
                if response.result.isSuccess{
                    print("Success!")
                    self.updateForJobTitles(json: JSON(response.result.value!))
                }else {
                    print("Error: \(String(describing: response.result.error))")
                }
        }
    }

    func updateForJobTitles(json: JSON) {
        if let jobs = json["jobs"].array {
            var return_jobs: [String] = []
            for job in jobs {
                return_jobs.append(job["title"].string!)
            }
            jobTitleView.text = "Here are entry-level jobs for \(self.majors) \n\n\(return_jobs)"
            
            let url = "https://api.indeed.com/ads/apisearch"
            Alamofire.request(url,
                              method: .get,
                              parameters: ["publisher": "8924341972846274",
                                           "l": "New York, New York",
                                           "q": return_jobs[0],
                                           "v": 2,
                                           "userip": "1.2.3.4",
                                           "useragent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2)",
                                           "format": "json"])
                    .responseJSON{response in
                        if response.result.isSuccess{
                            self.updateForJobPostings(json: JSON(response.result.value))
                        } else {
                            print("Error: ")
                            print("Error: \(String(describing: response.result.error))")
                        }
                    }
        }
    }

    func updateForJobPostings(json: JSON) {
        var resultString: String = ""
        if let jobPostings = json["results"].array {
            for posting in jobPostings {
                let title = posting["jobtitle"].string
                let company = posting["company"].string
                let snippet = posting["snippet"].string
                let jobKey = posting["jobkey"].string

                resultString = "\(resultString)\n\nTitle:\(title), company:\(company), snippet: \(snippet), key: \(jobKey)"
            }
            jobsView.text = resultString
        }
    }
    func retrieveJobPostings(jobTitle: String, location: String) -> [String] {
        return []
    }
    /*
    // MARK: - Navigation

    // In a storyboard-based application, you will often want to do a little preparation before navigation
    override func prepare(for segue: UIStoryboardSegue, sender: Any?) {
        // Get the new view controller using segue.destination.
        // Pass the selected object to the new view controller.
    }
    */

}
