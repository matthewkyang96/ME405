

class Controller:
    
    def __init__ (self):
        ''' doc string'''
        print('Creating Controller Driver')

    def set_point(self,theta_ref)
        print('Please input theta_ref')
        theta_ref = input()
        return theta_ref

    def control_gain(self)
        print('Please input K_p')
        K_p = input()
        return K_p
    
    def closed_loop(self,theta_measured,theta_ref,K_p):
        ''' doc string '''
        theta_error = theta_ref - theta_measured
        a = Kp * theta_error
        if a > 100:
            self.a_star = 100
        elif a < -100:
            self.a_star = -100
        else:
            self.a_star = a
        return self.a_star
    
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