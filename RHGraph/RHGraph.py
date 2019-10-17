# -*- coding: utf-8 -*-
"""
Created on Sun Jun 23 00:23:18 2019

@author: CHaithcock
"""

class RHGraph:
    
    """ Some related stuff so support working with Rush Hour Graph"""
    

    def generate_class_by_state(self,c,t,callback):
        """ Define a generator that produces all states  """
        
        """ standard algorithm:
            * bookeeping on cars/trucks available
            * bookeeping on current state of board (perhaps passed into recursion)
            * for each possible car placement in exit row:
                * place car in position given by loop iterator
                * call recursive function to place remaining cars/trucks
         """   

        pass
        
    
    def generate_class_by_state_recursion(self,c,t,pivot,callback):
        """ Run through recursion to place all of c cars and t trucks on
        the board"""
        
        """
        * for pivot to end of board
            * if possible, place horizontal car
                *call recursive function with c-1,t,updated pivot
            * if possible, place vertical car
            
            * if possible, place horizontal truck
            
            * if possible, place vertical truck
            
        """
        pass
    
    
    def generate_class_by_segment(self,c,t,callback):
        """
        """
        
        pass
    
    
    
    
    
    
    
