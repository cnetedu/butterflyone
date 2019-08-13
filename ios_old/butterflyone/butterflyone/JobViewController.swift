//
//  JobViewController.swift
//  butterflyone
//
//  Created by George Sequeira on 7/12/19.
//  Copyright © 2019 George Sequeira. All rights reserved.
//

import UIKit
import Alamofire
import SwiftyJSON

class JobViewController: UIViewController, UITableViewDelegate, UITableViewDataSource {
    var data: [CellData] = []

    func tableView(_ tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        return data.count
    }
    
    @IBOutlet weak var companyTable: UITableView!

    func tableView(_ tableView: UITableView, cellForRowAt indexPath: IndexPath) -> UITableViewCell {
        let cell = tableView.dequeueReusableCell(withIdentifier: "jobCell", for: indexPath) as! JobCell
        
//        cell.majorLabel.text = "A multiple"
//        cell.delegate = self
        let cellData: CellData = data[indexPath.item]

        cell.img.image = cellData.companyImage
        cell.descriptionLabel.text = cellData.description
        cell.headquartersLabel.text = cellData.headquarters
        cell.populationLabel.text = cellData.population
        cell.setStatusBar(pref: cellData.preference)
        cell.data = cellData
        return cell
    }


    func tableView(_ tableView: UITableView, didSelectRowAt indexPath: IndexPath) {
        let cellData: CellData = data[indexPath.item]
        let cell:JobCell = tableView.cellForRow(at: indexPath) as! JobCell
        cellData.updateEmployerPreference()
        cell.setStatusBar(pref: cellData.preference)
    }

    func tableView(_ tableView: UITableView, didDeselectRowAt indexPath: IndexPath) {
        let cellData: CellData = data[indexPath.item]
        let cell:JobCell = tableView.cellForRow(at: indexPath) as! JobCell
        cellData.updateEmployerPreference()
        cell.setStatusBar(pref: cellData.preference)
    }

    // Set spacing at top to be 0
    func tableView(_ tableView: UITableView, heightForHeaderInSection section: Int) -> CGFloat {
        return 0
    }

    var baseApi = "http://api.indeed.com/ads/apisearch?publisher=123412341234123"
                  + "&q=java+developer&l=austin%2C+tx&sort=&radius=&st=&jt=&start="
                  + "&limit=&fromage=&filter=&latlong=1&co=us&chnl=&userip=1.2.3.4"
                  + "&useragent=Mozilla/%2F4.0%28Firefox%29&v=2"

    @IBOutlet weak var employerTable: UITableView!
    
    override func viewDidLoad() {
        super.viewDidLoad()
        initCellData()
        companyTable.delegate = self
        companyTable.dataSource = self
        companyTable.register(UINib(nibName: "JobCell", bundle: nil), forCellReuseIdentifier: "jobCell")
        companyTable.rowHeight = 110
        companyTable.allowsMultipleSelection = true
        companyTable.separatorStyle = .none
        companyTable.separatorColor = .clear
        // Do any additional setup after loading the view.
    }
    
    func initCellData() {
//        cell.img.image = UIImage(named: "amazon2")
//        cell.label.text = "A voice speech company"
        let verizon: CellData = CellData(companyImage: UIImage(named:"verizon")!, description: "Multinational telecommunications conglomerate ", headquarters: "New York City, New York", population: "144,500", preference: .none)
        let facebook: CellData = CellData(companyImage: UIImage(named:"facebook")!, description: "Online social media and social networking service company", headquarters: "Menlo Park, CA", population: "30,275", preference: .none)
        let google: CellData = CellData(companyImage: UIImage(named:"google")!, description: " Technology company that specializes in Internet-related services and products", headquarters: "Mountain View, CA", population: "98,771", preference: .none)
        let morganStanley: CellData = CellData(companyImage: UIImage(named:"morganStanley")!, description: "Investment bank and financial services company.", headquarters: "Mountain View, CA", population: "98,771", preference: .none)
        let silverline: CellData = CellData(companyImage: UIImage(named: "silverline")!,
                                            description: "Enterprise Software", headquarters: "New York City, New York",
                                            population: "5,200", preference: .none)
        let calm: CellData = CellData(companyImage: UIImage(named:"calm")!, description: "Wellness software company", headquarters: "San Francisco, CA", population: "50", preference: .none)
        let amazon: CellData = CellData(companyImage: UIImage(named:"amazon")!, description: "E-commerce, cloud computing, digital streaming, and artificial intelligence.", headquarters: "Seattle, QA", population: "647,500", preference: .none)
        self.data.append(verizon)
        self.data.append(facebook)
        self.data.append(google)
        self.data.append(morganStanley)
        self.data.append(silverline)
        self.data.append(calm)
        self.data.append(amazon)
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
