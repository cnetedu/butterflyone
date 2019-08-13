//
//  LocationViewController.swift
//  butterflyone
//
//  Created by George Sequeira on 7/12/19.
//  Copyright © 2019 George Sequeira. All rights reserved.
//

import UIKit
import Magnetic

class LocationViewController: UIViewController, CustomSearchDelegate, MajorRemoval, UITableViewDelegate, UITableViewDataSource{
    func remove(data: String) {
        if let removalInd = self.selectedMajors.firstIndex(of: data) {
            self.selectedMajors.remove(at: removalInd)
            self.locationsTable.reloadData()
            self.searchField.isHidden = false
        }
        if self.selectedMajors.count  < 1 {
            self.nextButton.isHidden = true
        }
    }
    
    func optionSelected(data: String) {
        // We need to add the row here...
        self.selectedMajors.append(data)
        self.locationsTable.reloadData()
        
        if self.selectedMajors.count > 0 {
            self.nextButton.isHidden = false
            if self.selectedMajors.count > 2{
                self.searchField.isHidden = true
            }
        }
        else
        {
            self.nextButton.isHidden = true
        }
        self.searchField.text = ""
    }
    func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        return selectedMajors.count
    }
    
    func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {
        let cell = tableView.dequeueReusableCell(withIdentifier: "majorCell", for: indexPath) as! MajorCell
        
        cell.label.text = selectedMajors[indexPath.row]
        cell.delegate = self
        return cell
    }

    @IBOutlet weak var nextButton: UIButton!
    
    // Set the spacing between sections
    func tableView(_ tableView: UITableView, heightForHeaderInSection section: Int) -> CGFloat {
        return 2
    }
    
    func configureTableView(){
        locationsTable.rowHeight = 50
    }

    var selectedMajors: [String] = []

    @IBOutlet weak var searchField: CustomSearchTextField!
    @IBOutlet weak var locationsTable: UITableView!
    
    @IBOutlet weak var locationTextField: CustomSearchTextField!
    override func viewDidLoad() {
        super.viewDidLoad()
        searchField.dataList = [
            "Chicago, IL",
            "Dallas, TX",
            "Houston, TX",
            "Phoenix, AZ",
            "Philadelphia, PA",
            "New York, New York",
            "Seattle, WA",
            "Los Angeles, CA",
            "San Diego, CA"]
        searchField.searchDelegate = self
        
        locationsTable.delegate = self
        locationsTable.dataSource = self
        locationsTable.allowsSelection = false
        
        searchField.searchDelegate = self
        
        nextButton.isHidden = true
        nextButton.layer.cornerRadius = 10
        nextButton.clipsToBounds = true
        
        super.viewDidLoad()
        // Register a view
        locationsTable.register(UINib(nibName: "MajorCell", bundle: nil), forCellReuseIdentifier: "majorCell")
        locationsTable.separatorStyle = .none
        locationsTable.isScrollEnabled = false
        
        
        
        configureTableView()
    }
    override func prepare(for segue: UIStoryboardSegue, sender: Any?) {
        let defaults = UserDefaults.standard
        defaults.set(selectedMajors, forKey: "locations")
    }
}
