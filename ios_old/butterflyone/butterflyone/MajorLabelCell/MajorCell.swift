//
//  MajorCell.swift
//  butterflyone
//
//  Created by George Sequeira on 7/15/19.
//  Copyright © 2019 George Sequeira. All rights reserved.
//

import UIKit

protocol MajorRemoval {
    func remove(data: String)
}
class MajorCell: UITableViewCell {

    var delegate: MajorRemoval?
    
    @IBOutlet weak var colorVier: UIView!
    @IBOutlet weak var outerView: UIView!
    @IBOutlet weak var label: UILabel!

    override func awakeFromNib() {
        super.awakeFromNib()
        colorVier.layer.cornerRadius = 15
        colorVier.layer.masksToBounds = true
        label.numberOfLines = 1
        label.lineBreakMode = .byTruncatingTail
        label.adjustsFontSizeToFitWidth = false
    }

    @IBAction func closeClicked(_ sender: Any) {
        print("Hello Geo")
        delegate?.remove(data: self.label.text!)
    }
}
