class DBAgent:
    def book_appointment(self, patient_id: int, date: str, time: str):
        # Integrate with your database logic here
        return {"status": "success", "message": "Appointment booked successfully."}
    
    def get_appointments(self, patient_id: int):
        # Return dummy data for now
        return [{"id": 1, "date": "2025-03-01", "time": "10:00 AM"}]
    