//
//  MajorsViewController.swift
//  butterflyone
//
//  Created by George Sequeira on 7/12/19.
//  Copyright © 2019 George Sequeira. All rights reserved.
//

import UIKit
import iOSDropDown
class MajorsViewController: UIViewController, UITableViewDelegate, UITableViewDataSource, MajorRemoval, CustomSearchDelegate{
    // TODO: come back here.
    func remove(data: String) {
        if let removalInd = self.selectedMajors.firstIndex(of: data) {
            self.selectedMajors.remove(at: removalInd)
            self.majorTable.reloadData()
            self.customSearchTextField.isHidden = false
        }
        if self.selectedMajors.count  < 1 {
            self.careersButton.isHidden = true
        }
    }
    

    @IBOutlet weak var customSearchTextField: CustomSearchTextField!

    func optionSelected(data: String) {
        // We need to add the row here...
        self.selectedMajors.append(data)
        self.majorTable.reloadData()
        
        if self.selectedMajors.count > 0 {
            self.careersButton.isHidden = false
            if self.selectedMajors.count > 2{
                self.customSearchTextField.isHidden = true
            }
        }
        else
        {
            self.careersButton.isHidden = true
        }
        self.customSearchTextField.text = ""
    }

    var selectedMajors: [String] = []

    func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        return selectedMajors.count
    }
    
    func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {
        let cell = tableView.dequeueReusableCell(withIdentifier: "majorCell", for: indexPath) as! MajorCell
        
        cell.label.text = selectedMajors[indexPath.row]
        cell.delegate = self
        return cell
    }
    
    // Set the spacing between sections
    func tableView(_ tableView: UITableView, heightForHeaderInSection section: Int) -> CGFloat {
        return 2
    }

    func configureTableView(){
        majorTable.rowHeight = 50
    }
    
    @IBOutlet weak var majorTable: UITableView!
    @IBOutlet weak var careersButton: UIButton!

    var majors: [String] = []

    override func viewDidLoad() {
        var contents = ""
        let filepath = Bundle.main.path(forResource: "majors", ofType: "txt")!
        do {
            contents = try String(contentsOfFile: filepath)
        } catch {
            print("Could not load majors")
        }

        majorTable.delegate = self
        majorTable.dataSource = self
        majorTable.allowsSelection = false

        customSearchTextField.dataList = contents.components(separatedBy: "\n")
        customSearchTextField.searchDelegate = self

        careersButton.isHidden = true
        careersButton.layer.cornerRadius = 10
        careersButton.clipsToBounds = true

        super.viewDidLoad()
        // Register a view
        majorTable.register(UINib(nibName: "MajorCell", bundle: nil), forCellReuseIdentifier: "majorCell")
        majorTable.separatorStyle = .none
        majorTable.isScrollEnabled = false



        configureTableView()
    }

    override func prepare(for segue: UIStoryboardSegue, sender: Any?) {
        let defaults = UserDefaults.standard
        defaults.set(selectedMajors, forKey: "majors")
    }
}
