
# coding: utf-8

# In[32]:

import random
from environment import Agent, Environment
from planner import RoutePlanner
from simulator import Simulator
from collections import defaultdict



class LearningAgent(Agent):
    """An agent that learns to drive in the smartcab world."""

    def __init__(self, env):
        super(LearningAgent, self).__init__(env)  # sets self.env = env, state = None, next_waypoint = None, and a default color
        self.color = 'red'  # override color
        self.planner = RoutePlanner(self.env, self)  # simple route planner to get next_waypoint
        # TODO: Initialize any additional variables here
        self.qTable = dict()
        self.possibleActions=('forward','left','right',None)
        self.alpha=1
        self.gamma=0.4

    def reset(self, destination=None):
        self.planner.route_to(destination)
        # TODO: Prepare for a new trip; reset any variables here, if required
        self.alpha=1
        
        
    def maxQ(self,state):
        Qmax=list()
        for action in self.possibleActions:
            Qmax.append(self.qTable.get((state,action),0))
            
        
        return max(Qmax)  
       
    
    def choose_action(self,state):
        
        if random.random()<0.1:
             return random.choice(self.possibleActions) 
            
        allQ = list()
        
        for action in self.possibleActions:
            allQ.append(self.qTable.get((state,action),0))        
        chosenAction=list()
        for action in self.possibleActions:
            if self.qTable.get((state,action),0)==max(allQ):
                chosenAction.append(action)
        return random.choice(chosenAction)   

    

    def update(self, t):
        # Gather inputs
        self.next_waypoint = self.planner.next_waypoint()  # from route planner, also displayed by simulator
        inputs = self.env.sense(self)
        deadline = self.env.get_deadline(self)
        if t!=0:
            self.alpha=1/float(t)
        
        alpha=self.alpha
        print alpha
       
        # TODO: Update state
        self.state = (('light',inputs['light']),('oncoming',inputs['oncoming']),('right',inputs['right']),('left',inputs['left']),self.next_waypoint) 
        

        # TODO: Select action according to your policy
        #action = random.choice(self.possibleActions)
        action = self.choose_action(self.state)

        # Execute action and get reward
        reward = self.env.act(self, action)

        # TODO: Learn policy based on state, action, reward
        next_inputs = self.env.sense(self)
       
        next_state = (('light',next_inputs['light']),('oncoming',next_inputs['oncoming']),('right',next_inputs['right']),('left',next_inputs['left']),('next_waypoint',self.next_waypoint))        
        
        self.qTable[(self.state,action)]= self.qTable.get((self.state,action),0) + alpha*(reward+ self.gamma*(self.maxQ(next_state))-self.qTable.get((self.state,action),0))
                
        print "LearningAgent.update(): deadline = {}, inputs = {}, action = {}, reward = {}".format(deadline, inputs, action, reward)  # [debug]
        print len(self.qTable)





# In[ ]:

def run():
    """Run the agent for a finite number of trials."""

    # Set up environment and agent
    e = Environment()  # create environment (also adds some dummy traffic)
    a = e.create_agent(LearningAgent)  # create agent
    e.set_primary_agent(a, enforce_deadline=True)  # set agent to track

    # Now simulate it
    sim = Simulator(e, update_delay=0.1)  # reduce update_delay to speed up simulation
    sim.run(n_trials=100)  # press Esc or close pygame window to quit


if __name__ == '__main__':
    run()

