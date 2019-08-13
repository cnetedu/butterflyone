//
//  ReelViewController.swift
//  butterflyone
//
//  Created by George Sequeira on 7/16/19.
//  Copyright © 2019 George Sequeira. All rights reserved.
//

import UIKit
import iOSDropDown

class ReelViewController: UIViewController {

    @IBOutlet weak var searchField: DropDown!

    override func viewDidLoad() {
        super.viewDidLoad()
        // Do any additional setup after loading the view.
        searchField.optionArray = ["Opton 1", "2", "Option3"]
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
