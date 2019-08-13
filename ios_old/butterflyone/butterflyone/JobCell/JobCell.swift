//
//  JobCell.swift
//  butterflyone
//
//  Created by George Sequeira on 7/16/19.
//  Copyright © 2019 George Sequeira. All rights reserved.
//

import UIKit

enum EmployerPreference {
    case none
    case like
    case love
}

class CellData {
    let companyImage: UIImage
    let description: String
    let headquarters: String
    let population: String
    var preference: EmployerPreference

    init(companyImage: UIImage, description: String, headquarters: String, population: String, preference: EmployerPreference) {
        self.companyImage = companyImage
        self.description = description
        self.headquarters = headquarters
        self.population = population
        self.preference = preference
    }

    func updateEmployerPreference() {
        if preference == EmployerPreference.love {
            self.preference = EmployerPreference.none
        } else {
            if preference == EmployerPreference.like {
                self.preference = EmployerPreference.love
            }
            else {
                self.preference = EmployerPreference.like
            }
        }
    }

}

class JobCell: UITableViewCell {
    var data: CellData?

    @IBOutlet weak var status: UIImageView!

    @IBOutlet weak var descriptionLabel: UILabel!
    @IBOutlet weak var statusBar: UIView!
    @IBOutlet weak var innerView: UIView!
    @IBOutlet weak var img: UIImageView!
    @IBOutlet weak var headquartersLabel: UILabel!
    @IBOutlet weak var populationLabel: UILabel!
    
    override func awakeFromNib() {
        super.awakeFromNib()
        // Initialization code
        // We will use multi-select on these things.
        selectionStyle = .none
        status.layer.cornerRadius = 15
        status.layer.masksToBounds = true
        innerView.layer.cornerRadius = 6
        innerView.layer.masksToBounds = true
    }

    func setStatusBar(pref: EmployerPreference){
        print("My status: \(pref)")
        switch pref {
            case .none:
                statusBar.backgroundColor = .gray
                status.backgroundColor = .gray
                status.image = nil
            case .like:
                let blue: UIColor = UIColor(red:0.26, green:0.38, blue:1.00, alpha:1.0)
                statusBar.backgroundColor = blue
                status.backgroundColor = blue
                status.image = UIImage(named: "icons8-star-100")
            case .love:
                let green: UIColor = UIColor(red:0.13, green:0.76, blue:0.11, alpha:1.0)
                statusBar.backgroundColor = green
                status.backgroundColor = green
                status.image = UIImage(named: "icons8-heart-outline-100")
        }
    }
}
