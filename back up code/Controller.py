## @file Controller.py
#  Brief doc for Controller.py
#
#  Detailed doc for Controller.py 
#
#  @author Bryson Chan and Matthew Yang
#
#  @copyright License Info
#
#  @date April 24, 2019


class Controller:
    ''' 
    
    The proportional gain controller algorithm.  The class allows the user to control the position of the dc motor with varying proportional gain.
        
    '''
    
    def __init__ (self):
        ''' 
        Controller Constructor creates an instance of an object of the class Controller to be used with the following methods.
        
        '''
        print('Creating Controller Driver')

    def set_point(self,new_setpoint):
        '''
        This method receives the data from the user input reference position in a string, and converts this data type to an integer to be used. 
        
        @param new_setpoint - Reference position in string data type
        '''
        
        theta_ref = int(new_setpoint)
        return theta_ref

    def control_gain(self,new_Kp):
        '''
        This method receives the data from the user input gain in a string, and converts this data type to a float to be used.
        
        @param new_Kp -  Gain in string data type  
        '''
        K_p = float(new_Kp)
        return K_p
    
    def closed_loop(self,theta_measured,theta_ref,K_p):
        '''
        This method executes the proportional gain algorithm. The position input by the user is compared to the current position of the encoder. This difference in position is multiplied by the gain to adjust the motor duty cycle in order to reach the referenced position.
        
        @param theta_measured - The position read by the encoder
        @param theta_ref - The position input by the user
        @param K_p - The proportional gain input by the user
        '''
        
        theta_error = theta_ref - theta_measured
        a = K_p * theta_error
        if a > 100:
            a = 100
        elif a < -100:
            a = -100
        else:
            a = a
        return a
     

#    def pc_step(self):
#        '''doc string'''
#        a_s = 0
#        return a_s
#        print('please enter Kp')
#        self.Kp = input()
#        print('please enter theta ref')
#        self.theta_ref = input()
#        return self.theta_ref
#        return self.Kp
#    