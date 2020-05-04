//
//  ViewController.swift
//  IoTController
//
//  Created by Willie Shen on 4/22/20.
//  Copyright © 2020 Willie Shen. All rights reserved.
//

import UIKit

class ViewController: UIViewController {

    @IBOutlet weak var brightness: UILabel!
    
    //var currentValue:Double = 50.0
    
    @IBOutlet weak var adjuster: UISlider!
    override func viewDidLoad() {
        super.viewDidLoad()
        // Do any additional setup after loading the view.
        adjuster.maximumValue = 100.0
        
        adjuster.minimumValue = 0
        
        adjuster.value = 50
        //https://developer.apple.com/documentation/uikit/uislider#declarations
        
        brightness.text = "\(Int(adjuster.value))"
        
        //https://www.hackingwithswift.com/example-code/language/how-to-convert-a-float-to-an-int
        
    }

    @IBAction func valueChanged(_ sender: Any) {
        brightness.text = "\(Int(adjuster.value))"
        
    }
    
}

