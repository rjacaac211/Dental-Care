from .cv_agent import CVAgent
from .db_agent import DBAgent
from .web_search_agent import WebSearchAgent
import os

class SupervisorAgent:
    def __init__(self):
        # Initialize agents with necessary resources/paths
        model_path = os.path.json(os.path.dirname(__file__), "../models/oral_disease_model.h5")
        self.cv_agent = CVAgent
        self.db_agent = DBAgent()
        self.web_search_agent = WebSearchAgent()

    def handle_image_prediction(self, image_path: str):
        return self.cv_agent.predict(image_path)
    
    def handle_book_appointment(self, patient_id: int, date: str, time: str):
        return self.db_agent.book_appointment(patient_id, date, time)
    
    def handle_information_search(self, query: str):
        return self.web_search_agent.search_information(query)
    
if __name__ == "__main__":
    supervisor = SupervisorAgent()
    pred, conf = supervisor.handle_image_prediction("path_to_sample_image.jpg")
    print(f"Prediction: {pred}, Confidence: {conf}%")