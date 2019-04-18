

class Controller:
    
    def __init__ (self):
        ''' doc string'''
        print('Creating Controller Driver')
    
    def cloop(self,theta_measured,theta_ref):
        ''' doc string '''
        theta_error = theta_ref - theta_measured
        a = .5 * theta_error
        if a > 100:
            self.a_s = 100
        elif a < -100:
            self.a_s = -100
        else:
            self.a_s = a
        return self.a_s
    
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