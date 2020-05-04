//
//  ViewController.swift
//  IoTController
//
//  Created by Willie Shen on 4/22/20.
//  Copyright © 2020 Willie Shen. All rights reserved.
//

import UIKit
import CocoaMQTT
import CocoaAsyncSocket

class ViewController: UIViewController {

    @IBOutlet weak var brightness: UILabel!
    
    //var currentValue:Double = 50.0
    
    var mqtt: CocoaMQTT!
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
        
       //client.connect(host="eclipse.usc.edu", port=11000, keepalive=60)
        mqtt = CocoaMQTT(clientID: "123", host: "eclipse.usc.edu", port: 11000)
        
        // ...
        mqtt.subscribe("buttonpress")
        mqtt.subscribe("dimUpdate")
        
        mqtt.didReceiveMessage = { mqtt, message, id in
            
            print(message.topic)
            if(message.topic == "dimUpdate"){
                
                //https://www.hackingwithswift.com/example-code/language/how-to-convert-data-to-a-string
                var voltage:Int = Int(String(decoding:message.payload, as:UTF8.self)) ?? 0
                
                var brightnessLevel:Float = (Float(voltage)/1023) * 100
                self.adjuster.value = brightnessLevel
                
                self.brightness.text = "\(Int(self.adjuster.value))"
                
                print("received")
                
                
                
            }
            
            
        }
        _ = mqtt.connect()
        
    }

    @IBAction func valueChanged(_ sender: Any) {
        brightness.text = "\(Int(adjuster.value))"
        
        var brightness:Int = (Int)(1023 * (Double(Int(adjuster.value)) / 100.0))
        var voltage:Double = Double(brightness * 5)/1023.0
        
        mqtt.publish("buttonpress", withString: "\(brightness)" )
    }
    
}

