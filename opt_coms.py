import numpy as np 
import matplotlib.pyplot as plt 

def db_to_dec(number):
    return 10**(number/10)    
class optical_switch():
    
    def __init__(self, input1, input2, state: bool,extinctratio, id, cross_talk_input1 = None, cross_talk_input2 = None):
        
        """_summary_

        Args:
            input1 (_type_): INPUT 1
            input2 (_type_): INPUT 2 
            state (bool): STATE OF SWITCH: ON/OFF
            extinctratio (_type_): dB scale
        """
        self.id         = id        #   Box No.
        self.input1dbm  = input1    #   dBm
        self.input1     = db_to_dec(self.input1dbm - 30) #Watt
        self.input2dbm  = input2    #   dBm
        self.input2     = db_to_dec(self.input2dbm - 30) #Watt
        
        self.state      = state     #   On or Off
        self.output1    = None      
        self.output2    = None
        self.extinctratiodb= extinctratio     # dB
        self.extinctratio = db_to_dec(self.extinctratiodb) #Watt
        
        self.cross_talk_input1dbm  =   cross_talk_input1
        self.cross_talk_input1    =   None
        if self.cross_talk_input1dbm is not None:
            self.cross_talk_input1 = db_to_dec(self.cross_talk_input1dbm - 30) #Watt
           
        
        self.cross_talk_input2    =   None
        self.cross_talk_input2dbm  =   cross_talk_input2
        if self.cross_talk_input2dbm is not None:
            self.cross_talk_input2 = db_to_dec(self.cross_talk_input2dbm - 30) #Watt
        
        
    def change_state(self):
        """
            Changes switch state (ON/OFF)
        """
        self.state = not self.state
    
    def get_outputs(self):
        #ASSUME SWITCH IS OFF!
        self.cross_talk1= (1/(self.extinctratio+1))*self.input2
        self.cross_talk2= (1/(self.extinctratio+1))*self.input1

        self.output1    = (self.extinctratio/(self.extinctratio+1))*self.input1 + self.cross_talk1
        self.output2    = (self.extinctratio/(self.extinctratio+1))*self.input2 + self.cross_talk2
        #CROSS TALK FROM INPUT SIGNAL
        # Ο1 = (1/er+1)*I2
        # Ο2 = (1/er+1)*I1
        
        
        #CROSS TALK FROM INPUT CROSS TALK - ADDED IF NOT NONE
        if self.cross_talk_input1 is not None:
            # CO1 += (er/er+1)*CI1
            # CO2 += (er/er+1)*CI2
            self.cross_talk1    += (self.extinctratio/(self.extinctratio+1))*self.cross_talk_input1 
            self.cross_talk2    += (self.extinctratio/(self.extinctratio+1))*self.cross_talk_input2
        
        #IF ON THEN SWAP THE RESULTS
        if self.state:#an einai 1 einai on opote exeis anapodi leitoyrgia
        
            self.output1,self.output2           =self.output2, self.output1    
            self.cross_talk1, self.cross_talk2  = self.cross_talk2, self.cross_talk1
        self.output1dbm = 10*np.log10(self.output1) + 30
        
        self.output2dbm = 10*np.log10(self.output2) + 30
        
        self.cross_talk1dbm= 10*np.log10(self.cross_talk1) + 30
        self.cross_talk2dbm= 10*np.log10(self.cross_talk2) + 30
        
    def get_state(self):
        if self.state:
            return "ON"
        return  "OFF"
    
    def print_output(self):
        print("\033[31mSWITCH   :   \033[0m",self.id)
        print("STATE    :   ",self.get_state())
        print("ER       :   ",self.extinctratio)
        CrossInTalk1     = "None"
        CrossInTalk1dbm  = "None"
        if self.cross_talk_input1 is not None:
            CrossInTalk1  = np.round(self.cross_talk_input1*1e3,5)
            CrossInTalk1dbm = np.round( self.cross_talk_input1dbm,2)
            
        CrossInTalk2    = "None"
        CrossInTalk2dbm = "None"
        if self.cross_talk_input2 is not None:
            CrossInTalk2  = np.round(self.cross_talk_input2*1e3,5)
            CrossInTalk2dbm = np.round( self.cross_talk_input2dbm,2)
        print("Input Values              "+"-"*35)
        print("In- Cross Talk 1 ----->   ","{:<10} mW   or  {:<10} dBm".format(CrossInTalk1,CrossInTalk1dbm  ))  
        print("In- Cross Talk 2 ----->   ","{:<10} mW   or  {:<10} dBm".format(CrossInTalk2,CrossInTalk2dbm  ))
        print("Input  1         ----->   ","{:<10} mW   or  {:<10} dBm".format(np.round(self.input1*1e3,5)  ,np.round(self.input1dbm,2)   ))  
        print("Input  2         ----->   ","{:<10} mW   or  {:<10} dBm".format(np.round(self.input2*1e3,5)  ,np.round(self.input2dbm,2)   ))  
        print("Output Values             "+"-"*35)
        print("Out- Cross Talk 1----->   ","{:<10} mW   or  {:<10} dBm".format(np.round(self.cross_talk1*1e3,5)  ,np.round(self.cross_talk1dbm,2)   ))
        print("Out- Cross Talk 2----->   ","{:<10} mW   or  {:<10} dBm".format(np.round(self.cross_talk2*1e3,5)  ,np.round(self.cross_talk2dbm,2)   ))
        print("Output 1         ----->   ","{:<10} mW   or  {:<10} dBm".format(np.round(self.output1*1e3,5)  ,np.round(self.output1dbm,2)   ))  
        print("Output 1         ----->   ","{:<10} mW   or  {:<10} dBm".format(np.round(self.output2*1e3,5)  ,np.round(self.output2dbm,2)   ))  
        print("_"*61)



if __name__ == "__main__":
    states = []
    input_values ={"I0":0, "I1":0,"I2":0, "I3":0}
    switches     ={"Switch 0":None, "Switch 1":None, "Switch 3":None}
    print("Welcome to the Optical Switch Management System")
    print("I0 ------>           --------->      ------>          -------")
    print("                      SWITCH0                         SWITCH1")
    print("I1 ------>           ---------\u2198      ------>          >------")

    print("I2 ------>           ---------\u2197      ------>          >------")
    print("                      SWITCH2                         SWITCH3")
    print("I3 ------>           --------->      ------>          -->----")

    
    for m in range(4):
        
        while(1):
            x=input(f"State {m} (ON/OFF):")
            
            if x=="ON" or x=="OFF":
                states.append(x)
                
                break
            else:
                print("Invalid Input, Available Values: ON/OFF.")
        s = input_values.keys()[m]
        input_values[m] = input(s+" (dBm) : ")
    
 
    box0 = optical_switch(0, 0 , False, 20, id = 0)    
    box0.get_outputs()
    box0.print_output()
    box2 = optical_switch(0, 0 , True, 20, id = 2)   
    box2.get_outputs()
    box2.print_output()
    from time import sleep
    sleep(0.5)
    box1 = optical_switch(box0.output1dbm, box2.output2dbm , False, 20, id = 1, cross_talk_input1=box0.cross_talk1dbm, cross_talk_input2=box2.cross_talk1dbm)   
    box1.get_outputs()
    box1.print_output()
    sleep(0.5)
    box3 = optical_switch(box2.output1dbm, box0.output2dbm , True, 20, id = 3, cross_talk_input1=box0.cross_talk2dbm, cross_talk_input2=box2.cross_talk2dbm)
    box3.get_outputs()
    box3.print_output()