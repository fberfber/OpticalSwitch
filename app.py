from opt_coms import optical_switch 
from time import sleep
import matplotlib.pyplot as plt
from matplotlib.widgets import Button, TextBox
import numpy as np 
class SwitchNetwork:
    def __init__(self, inputs:list, states:list, ER):
        self.inputs = inputs
        self.states = states
        self.ER     = ER
        switch_0 = optical_switch( inputs[0],inputs[1], states[0], extinctratio= ER, id =0)
        switch_0.get_outputs()
        switch_2 = optical_switch( inputs[2],inputs[3], states[2], extinctratio= ER, id =2)
        switch_2.get_outputs()
        sleep(0.08)
        switch_1 = optical_switch(switch_0.output1dbm, switch_2.output2dbm , states[1], ER, id = 1, cross_talk_input1=switch_0.cross_talk1dbm, cross_talk_input2=switch_2.cross_talk1dbm)   
        sleep(0.08)
        switch_3 = optical_switch(switch_2.output1dbm, switch_0.output2dbm ,  states[3], ER, id = 3, cross_talk_input1=switch_0.cross_talk2dbm, cross_talk_input2=switch_2.cross_talk2dbm)
        self.switches = [switch_0, switch_1,switch_2, switch_3]
        
        self.fig, self.ax = plt.subplots()
        self.ax.set_title("Optical Switch Network Manager", fontdict={
        'fontsize': 30,
        'fontweight': 'bold',
        'color': '#222211',  # Dark grey for a modern look
        'family': 'sans-serif',
        })

        self.ax.set_facecolor("#ffffff")  # White axes background
        self.ax.tick_params(colors='#555555')  # Muted tick color
        self.ax.spines['top'].set_visible(False)
        self.ax.spines['right'].set_visible(False)
        self.buttons = []
       
        for i in range(4):
            bx = plt.axes([0.15+ i*0.2, 0.05, 0.1, 0.075])
            button = Button(bx, label=f"Toggle {i}")
            button.label.set_fontsize(20)
            button.label.set_fontweight("bold")
            button.on_clicked(lambda event, idx=i: self.toggle_button(event, idx))
            self.buttons.append(button)
        
        # Create four text boxes
        self.textboxes = []
        places = [[0.08, 0.265], [0.08, 0.358],[0.08, 0.724],[0.08, 0.817] ]
        for i in range(4):
            axbox =  plt.axes([0.1,places[i][1], 0.07, 0.035]) # [left, bottom, width, height]
            textbox = TextBox(axbox, f"Input {3-i}(dBm): ", initial="0")
            textbox.label.set_fontsize(17)
            textbox.on_submit(lambda input, label=3-i: self.change_inputs(label, input))
            self.textboxes.append( textbox)

    def update_switch(self,id):
        if id == 1:
            self.switches[1]    = optical_switch(self.switches[0].output1dbm, self.switches[2].output2dbm , self.states[1], self.ER, id = 1, cross_talk_input1=self.switches[0].cross_talk1dbm, cross_talk_input2=self.switches[2].cross_talk1dbm) 
        elif id == 3:
            self.switches[3]    = optical_switch(self.switches[2].output1dbm, self.switches[0].output2dbm ,  self.states[3], self.ER, id = 3, cross_talk_input1=self.switches[0].cross_talk2dbm, cross_talk_input2=self.switches[2].cross_talk2dbm)
        elif id ==0:
            self.switches[0] = optical_switch( self.inputs[0],self.inputs[1], self.states[0], extinctratio= self.ER, id =0)
            self.switches[0].get_outputs()
            sleep(0.08)
            self.switches[1]    = optical_switch(self.switches[0].output1dbm, self.switches[2].output2dbm , self.states[1], self.ER, id = 1, cross_talk_input1=self.switches[0].cross_talk1dbm, cross_talk_input2=self.switches[2].cross_talk1dbm) 
            self.switches[3]    = optical_switch(self.switches[2].output1dbm, self.switches[0].output2dbm ,  self.states[3], self.ER, id = 3, cross_talk_input1=self.switches[0].cross_talk2dbm, cross_talk_input2=self.switches[2].cross_talk2dbm)
        elif id == 2:
            self.switches[2] = optical_switch( self.inputs[2],self.inputs[3], self.states[2], extinctratio= self.ER, id =2)
            self.switches[2].get_outputs()
            sleep(0.08)
            self.switches[1]    = optical_switch(self.switches[0].output1dbm, self.switches[2].output2dbm , self.states[1], self.ER, id = 1, cross_talk_input1=self.switches[0].cross_talk1dbm, cross_talk_input2=self.switches[2].cross_talk1dbm) 
            self.switches[3]    = optical_switch(self.switches[2].output1dbm, self.switches[0].output2dbm ,  self.states[3], self.ER, id = 3, cross_talk_input1=self.switches[0].cross_talk2dbm, cross_talk_input2=self.switches[2].cross_talk2dbm)
        else:
            print("updating all with ",self.inputs, self.states)
            self.switches[0] = optical_switch( self.inputs[0],self.inputs[1], self.states[0], extinctratio= self.ER, id =0)
            self.switches[2] = optical_switch( self.inputs[2],self.inputs[3], self.states[2], extinctratio= self.ER, id =2)
            self.switches[2].get_outputs()
            
            self.switches[0].get_outputs()
            sleep(0.08)
            self.switches[1] = optical_switch(self.switches[0].output1dbm, self.switches[2].output1dbm , self.states[1], self.ER, id = 1, cross_talk_input1=self.switches[0].cross_talk1dbm, cross_talk_input2=self.switches[2].cross_talk1dbm)   
            self.switches[3] = optical_switch(self.switches[0].output2dbm, self.switches[2].output2dbm , self.states[3], self.ER, id = 3, cross_talk_input1=self.switches[0].cross_talk2dbm, cross_talk_input2=self.switches[2].cross_talk2dbm)   
            self.switches[1].get_outputs()
            self.switches[3].get_outputs()
    def set_inputs(self, new_inputs:list):
        self.inputs = new_inputs
        self.update_switch(-1)
    def set_states(self,new_states):
        self.states = new_states
    def toggle_switch(self, id):
        if id ==-1:
            
            self.states = [not s for s in self.states]

        else:
           
            self.states[id] = not self.states[id]
      
        self.update_switch(-1)
    def get_outputs(self):
    
        self.switches[0].get_outputs()
        self.switches[2].get_outputs()
        sleep(0.08)
        self.switches[3].get_outputs()
        sleep(0.08)    
        self.switches[1].get_outputs()
        sleep(0.02)
        out =[self.switches[1].output1dbm, self.switches[1].output2dbm, self.switches[3].output1dbm, self.switches[3].output2dbm], [self.switches[1].cross_talk1dbm , self.switches[1].cross_talk2dbm, self.switches[3].cross_talk1dbm, self.switches[3].cross_talk2dbm ]
     
        return out

    def show_gui(self):
        plt.show()
    def set_gui(self):
       
        c = []
        for s in self.states:
            if s:
                c.append("green")
            else:
                c.append("red")
        self.ax.clear()
        self.ax.set_title("Optical Switch Network Manager", fontdict={
        'fontsize': 30,
        'fontweight': 'bold',
        'color': '#222211',  # Dark grey for a modern look
        'family': 'sans-serif',
        })

        self.ax.set_facecolor("#ffffff")  # White axes background
        self.ax.tick_params(colors='#555555')  # Muted tick color
        self.ax.spines['top'].set_visible(False)
        self.ax.spines['right'].set_visible(False)
        self.ax.set_xlim(0, 5)
        self.ax.set_ylim(0, 5)
        self.ax.axis('off')

        # Buttons
        self.ax.add_patch(plt.Rectangle((1, 4), 1.5, 0.8, color=c[0]))
        self.ax.text(1.75, 4.4, f"Switch {0}", va='center', ha='center', color='white', fontsize=17)
        self.ax.add_patch(plt.Rectangle((3, 4), 1.5, 0.8, color=c[1]))
        self.ax.text(3.75, 4.4, f"Switch {1}", va='center', ha='center', color='white', fontsize=17)
        self.ax.add_patch(plt.Rectangle((1, 1), 1.5, 0.8, color=c[2]))
        self.ax.text(1.75, 1.4, f"Switch {2}", va='center', ha='center', color='white', fontsize=17)
        self.ax.add_patch(plt.Rectangle((3, 1), 1.5, 0.8, color=c[3]))
        self.ax.text(3.75, 1.4, f"Switch {3}", va='center', ha='center', color='white', fontsize=17)
        # ____________________________________________________________
        #self.ax.text(0.2, 4.7, f"Input 0: {self.inputs[0]}", va='center', ha='center', color='black', fontsize=17)
        self.ax.plot([0.6, 1], [4.7, 4.7], color='blue', linewidth=2)
        self.ax.plot([2.5, 3], [1, 1], color='black', linewidth=2)
        #self.ax.text(0.2, 4.1, f"Input 1: {self.inputs[1]}", va='center', ha='center', color='black', fontsize=17)
        self.ax.plot([2.5, 3], [1.8, 4], color='black', linewidth=2)
        self.ax.plot([0.6, 1], [4.1, 4.1], color='blue', linewidth=2)
        # ____________________________________________________________
        #self.ax.text(0.2, 1.7, f"Input 2: {self.inputs[2]}", va='center', ha='center', color='black', fontsize=17)
        self.ax.plot([0.6, 1], [1.7, 1.7], color='blue', linewidth=2)
        self.ax.plot([2.5, 3], [4.8, 4.8], color='black', linewidth=2)
        #self.ax.text(0.2, 1.1, f"Input 3: {self.inputs[3]}", va='center', ha='center', color='black', fontsize=17)
        self.ax.plot([0.6, 1], [1.1, 1.1], color='blue', linewidth=2)
        self.ax.plot([2.5, 3], [4, 1.8], color='black', linewidth=2)
        # ____________________________________________________________
      
        signal,crosstalk =self.get_outputs()
        print(self.states)
        print(signal)
        print(crosstalk)
        signal = [np.round(k,2) for k in signal]
        crosstalk = [np.round(k,2) for k in crosstalk]
        self.ax.text(4.55, 4.9, f"OUT 0: {signal[0]} dBm", va='center', ha='center', color='black', fontsize=17)
        self.ax.text(4.55, 5.1, f"CROSSTALK: {crosstalk[0]} dBm", va='center', ha='center', color='black', fontsize=17)
        self.ax.plot([4.5, 5], [4.7, 4.7], color='black', linewidth=2)
        self.ax.plot([4.5, 5], [4.1, 4.1], color='black', linewidth=2)
        self.ax.text(4.55, 3.9, f"OUT 1: {signal[1]} dBm", va='center', ha='center', color='black', fontsize=17)
        self.ax.text(4.55, 3.7, f"CROSSTALK: {crosstalk[1]} dBm", va='center', ha='center', color='black', fontsize=17)
        # ____________________________________________________________
        self.ax.text(4.55, 2.1, f"OUT 2: {signal[2]} dBm", va='center', ha='center', color='black', fontsize=17)
        self.ax.text(4.55, 1.9, f"CROSSTALK: {crosstalk[2]} dBm", va='center', ha='center', color='black', fontsize=17)
        self.ax.plot([4.5, 5], [1.1, 1.1], color='black', linewidth=2)
        self.ax.plot([4.5, 5], [1.7, 1.7], color='black', linewidth=2)
        self.ax.text(4.55, 0.7, f"CROSSTALK: {crosstalk[3]} dBm", va='center', ha='center', color='black', fontsize=17)
        self.ax.text(4.55, 0.9, f"OUT 3: {signal[3]} dBm", va='center', ha='center', color='black', fontsize=17)
        # ____________________________________________________________
        plt.draw()
        plt.subplots_adjust(left = 0, right =1)
    def change_inputs(self,label,input):
        input = float(input)
        input = np.round(input,2)
        self.inputs[label] = input
        self.set_inputs(new_inputs=self.inputs )
    
        self.set_gui()
    def toggle_button(self,event,id):
      
        self.toggle_switch(id)
        sleep(0.02)
        self.set_gui()

if __name__ == "__main__":
    """
    MyNetwork = SwitchNetwork(inputs=[0,0,0,0], states=[True, True, False, False], ER =20)
    MyNetwork.get_outputs()
    app = GUI_Manager(MyNetwork)
    app.set_gui()
    app.show_gui()
    """
    MyNetwork = SwitchNetwork(inputs=[0,0,0,0], states=[True, True, False, False], ER =20)
    MyNetwork.set_gui()
    MyNetwork.show_gui()