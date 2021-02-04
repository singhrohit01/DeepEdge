
from helpers.timer import Timer
from helpers.mock_input_generator import MockInputGenerator
from helpers.util import echo
from os import path

# Performs model execution
class AbstractWorkload:

    def __init__(self):        
        self._input_generator = MockInputGenerator(limit = 100) # TODO: reduce the limit if the device doesn't have enough space to retrieve all the images at once
        self._timer = Timer()
        self._result = None

    def getModel(self):
        raise NotImplementedError("Model not set") 

    def getFramework(self):
        raise NotImplementedError("Framework not set")

    def getApplication(self):
        raise NotImplementedError("Application not set")

    def getModelToUse(self):
        raise NotImplementedError("Please supply the model file to be used")

    def __getModelFile(self):
        """ Run the model on the given input data ; Return the accuracy"""
        return path.join('./models', self.getModelToUse())

    def start(self, msg_queue, results_queue):
        """
            This method will be called by a thread
            Hence, all the messaging/communication is done using the msg_queue
        """

        try:
    
            result = {}

            ### Prepare data/input
            echo ("Fetching input data")
            input_data = self._input_generator.next_input()

            if input_data is not None:

                result["input_id"] = input_data["id"]    

                echo ("Starting model execution")

                msg_queue.put("START")
                msg_queue.join()

                self._timer.start()

                ### Start Inference
                result["accuracy"] = self._run_model(input_data, self.__getModelFile())
                
                self._timer.stop()
                
                echo ("Model execution complete")

                msg_queue.put("STOP")
                msg_queue.join()

                result["start_time"] = self._timer.start_time()
                result["end_time"] = self._timer.end_time()
                result["inference_time"] = self._timer.diff()

            else:
                print("Out of input")
                msg_queue.put("STOP")
                msg_queue.join()

            echo ("Sending inference result")
            results_queue.put(result)

        except Exception as e:
            echo ("ERROR when executing workload - {}".format(e))
            msg_queue.put("STOP")
            msg_queue.join()
            results_queue.put({})

    def _run_model(self, input_data, model_file):        
        """ Run the model on the given input data ; Return the accuracy"""
        raise NotImplementedError("Model run method not implemented")