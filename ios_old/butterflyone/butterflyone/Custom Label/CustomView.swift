//
//  CustomView.swift
//  butterflyone
//
//  Created by George Sequeira on 7/15/19.
//  Copyright © 2019 George Sequeira. All rights reserved.
//

import UIKit

protocol CustomButtonDelegate {
    func deleteClicked(_ view: UIView, _ sender: UIButton)
}

class CustomView: UIView {

    @IBOutlet weak var button: UIButton!
    @IBOutlet weak var label: UILabel!
    @IBOutlet var contentView: UIView!
    var delegate: CustomButtonDelegate?

    override init(frame: CGRect) {
        super.init(frame:frame)
        commonInit()
    }
    
    required init?(coder aDecoder: NSCoder) {
        super.init(coder: aDecoder)
        commonInit()
    }
    
    private func commonInit() {
        Bundle.main.loadNibNamed("CustomView", owner: self, options: nil)
        
        contentView.frame = self.bounds
        contentView.autoresizingMask = [.flexibleHeight, .flexibleWidth]
        addSubview(contentView)
    }
    @IBAction func buttonPressed(_ sender: UIButton) {
        self.delegate?.deleteClicked(self, sender)
    }
    
}
