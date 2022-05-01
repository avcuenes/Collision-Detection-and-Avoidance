""" 
Mehmet Enes AVCU
"""
import numpy as np

class KalmanFilter:
    def __init__(self):
        
        pass
    
    def define_number_of_state(self):
        """
        This function update number of states
        """
        self.number_of_state = 6
    
    def define_number_of_measured_state(self):
        """
        This function update number of measured_state
        """
        self.number_of_measure_state = 3
    
    def define_number_of_elements_input_variable(self):
        """
        This function update number of input variable
        """
        self.number_of_input_variable = 5
    
    def define_state_transition_matrix(self):
        """
        This function define kalman matrix
        """
        self.State_transition_matrix = np.zeros([self.number_of_state, self.number_of_state])
        pass
    
    def define_observation_matrix(self):
        """
        This function define observation matrix
        """
        self.Observation_matrix = np.zeros([self.number_of_measure_state, self.number_of_state])
    
    def define_control_matrix(self):
        """
        This function define control matrix
        """
        self.control_matrix = np.zeros([self.number_of_state, self.number_of_input_variable])
    
    def define_estimate_uncertanity_matrix(self):
        """
        This function define estimare uncertanity matrix
        """
        self.estimate_uncertanity_matrix = np.zeros([self.number_of_state, self.number_of_state])
    
    def define_process_noise_uncertanity_matrix(self):
        """
        This function define process noise uncertanity matrix
        """
        self.process_noise_uncertanity_matrix = np.zeros([self.number_of_state, self.number_of_state])
    
    def define_measurement_uncertanity_matrix(self):
        """
        This function define measurement uncertanity matrix
        """
        self.measurement_uncertanity_matrix = np.zeros([self.number_of_measure_state, self.number_of_measure_state])
    
    def define_kalman_gain_matrix(self):
        """
        This function define kalman gain matrix
        """
        self.kalman_gain_matrix = np.zeros([self.number_of_state, self.number_of_measure_state])
    
    def define_process_noise_vector(self):
        """
        This function define process noise vector
        """
        self.process_noise_vector = np.zeros([self.number_of_state, 1])
    
    def define_measurement_noise_vector(self):
        """
        This function define measurement noise vector
        """
        self.measurement_noise_vector = np.zeros([self.number_of_measure_state, 1])
    
    def define_state_vector(self):
        """
        This function define state vector
        """
        self.state_vector = np.zeros([self.number_of_state, 1])
    
    def define_output_vector(self):
        """
        This function define output vector
        """
        self.output_vector = np.zeros([self.number_of_measure_state, 1])
    
    def define_input_variable(self):
        """
        This function define input variable
        """
        self.input_variable = np.zeros([self.number_of_input_variable, 1])
    
    def define_dimensions_notation(self):
        """
        This function define notation of problem
        """
        self.define_number_of_elements_input_variable()
        self.define_number_of_measured_state()
        self.define_number_of_state()
    
    def define_notation_of_problem(self):
        """
        This function define notation of problem
        """
        self.define_control_matrix()
        self.define_estimate_uncertanity_matrix()
        self.define_input_variable()
        self.define_observation_matrix()
        self.define_kalman_gain_matrix()
        self.define_measurement_noise_vector()
        self.define_measurement_uncertanity_matrix()
        self.define_output_vector()
        self.define_process_noise_uncertanity_matrix()
        self.define_state_vector()
        self.define_state_transition_matrix()
        self.define_process_noise_vector()
    
    def update_delta_time(self):
        """
        This function update hertz of process 
        """
        self.delta_time = 0.01 # hertz
    
    def calculate_standart_deviation_of_acceleration(self):
        """
        This function calculate standart deviation of acceleration
        """
        self.standart_deviation = 1
    
    def calcuate_variance_of_acceleration(self):
        """
        This function calculate_variance of acceleration
        """
        self.variance = np.power(self.standart_deviation,2)
        
    def calculate_state_transition_matrix(self):
        """
        This function calculate state transition matrix denoted by F
        """
        for i in range(0,self.number_of_state):
            self.State_transition_matrix[i][i] = 1
            if i%2 == 0:
                self.State_transition_matrix[i][i+1] = self.delta_time
    
    def calculate_process_noise_matrix(self):
        """
        This function calculate process noise matrix
        """
        Q_a = np.zeros([self.number_of_state, self.number_of_state])
        Q_a[1][1] = 1
        Q_a[3][3] = 1
        Q_a[5][5] = 1
        
        self.process_noise_uncertanity_matrix = np.matmul(np.matmul(self.State_transition_matrix,Q_a),self.State_transition_matrix.transpose())
        self.process_noise_uncertanity_matrix = self.process_noise_uncertanity_matrix*self.variance
    
    def calculate_observation_matrix(self):
        """
        This function calculate observation matrix
        """
        self.Observation_matrix[0][1] = 1
        self.Observation_matrix[1][3] = 1
        self.Observation_matrix[2][5] = 1
        
    def Run(self):
        self.define_dimensions_notation()
        self.define_notation_of_problem()



if __name__=="__main__":
    a = KalmanFilter()
    
    a.Run()
    
        
        
    
    