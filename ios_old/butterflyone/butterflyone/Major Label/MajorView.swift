//
//  MajorView.swift
//  butterflyone
//
//  Created by George Sequeira on 7/15/19.
//  Copyright © 2019 George Sequeira. All rights reserved.
//

import UIKit

class MajorView: UIView {
    @IBOutlet var contentView: UIView!
    @IBOutlet weak var label: UILabel!
    @IBOutlet weak var button: UIButton!

    override init(frame: CGRect) {
        super.init(frame:frame)
        commonInit()
    }
    
    required init?(coder aDecoder: NSCoder) {
        super.init(coder: aDecoder)
        commonInit()
    }
    
    private func commonInit() {
        // we're going to do stuff here.
        let nib = Bundle.main.loadNibNamed("MajorView", owner: self, options: nil)
        
        contentView.frame = self.bounds
        contentView.autoresizingMask = [.flexibleHeight, .flexibleWidth]
        addSubview(contentView)
    }
}
