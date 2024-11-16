import heapq
from datetime import datetime
import threading
import time
import random

class Patient:
    def __init__(self, name, age, sex):
        """
        Initialize the Patient object with name, age, sex, arrival time, and ESI priority.
        """
        self.name = name
        self.age = age
        self.sex = sex
        self.arrival_time = datetime.now()  # Automatically set the arrival time to the current time
        self.esi_priority = None

    def calculate_esi_priority(self):
        """
        Method to calculate the ESI priority of the patient based on input.
        """
        print(f"\nPatient Name: {self.name}, Age: {self.age}, Sex: {self.sex}, Arrival Time: {self.arrival_time.strftime('%Y-%m-%d %H:%M:%S')}")

        # Step 1: Check for life-saving interventions (ESI-1)
        life_saving = input("Does the patient need life-saving interventions? (yes/no): ").strip().lower()
        if life_saving == "yes":
            print("Checking for critical conditions...")
            physical_injury = input("Does the patient have severe physical injuries? (yes/no): ").strip().lower()
            if physical_injury == "yes":
                self.esi_priority = 1
                return self._display_priority()

            cardiac_arrest = input("Is the patient experiencing cardiac arrest? (yes/no): ").strip().lower()
            if cardiac_arrest == "yes":
                self.esi_priority = 1
                return self._display_priority()

            respiratory_distress = input("Is the patient in respiratory distress? (yes/no): ").strip().lower()
            if respiratory_distress == "yes":
                self.esi_priority = 1
                return self._display_priority()

        # Step 2: Check for severe pain or high-risk conditions (ESI-2)
        severe_pain = input("Is the patient experiencing severe pain? (yes/no): ").strip().lower()
        if severe_pain == "yes":
            chest_pain = input("Does the patient have chest pain? (yes/no): ").strip().lower()
            migraines = input("Does the patient have severe migraines? (yes/no): ").strip().lower()
            accident = input("Has the patient been in an accident? (yes/no): ").strip().lower()

            if chest_pain == "yes" or migraines == "yes" or accident == "yes":
                self.esi_priority = 2
                return self._display_priority()

        # Step 3: Check for resource needs (ESI-3 or ESI-4)
        scans_needed = input("Does the patient need scans or tests? (yes/no): ").strip().lower()
        if scans_needed == "yes":
            try:
                num_scans = int(input("How many scans/tests are required? (enter a number): "))
            except ValueError:
                print("Invalid input. Number of scans must be an integer.")
                return

            scan_types = input("What types of scans/tests are needed? (e.g., X-ray, CT scan): ").strip()

            if num_scans > 1:
                self.esi_priority = 3
                return self._display_priority()
            else:
                self.esi_priority = 4
                return self._display_priority()

        # Step 4: No urgent needs (ESI-5)
        self.esi_priority = 5
        return self._display_priority()

    def _display_priority(self):
        """
        Display the calculated ESI priority.
        """
        print(f"ESI Priority for {self.name}: Level {self.esi_priority}")
        return self.esi_priority

    def __lt__(self, other):
        """
        Custom less-than method for priority queue.
        Patients are compared first by priority, then by arrival time.
        """
        if self.esi_priority == other.esi_priority:
            return self.arrival_time < other.arrival_time
        return self.esi_priority < other.esi_priority

    def __repr__(self):
        return f"Patient({self.name}, Priority={self.esi_priority})"


class PatientManager:
    def __init__(self):
        """
        Initialize the PatientManager with a min-heap for storing patients and a condition variable to notify the ICU.
        """
        self.patients = []
        self.lock = threading.Lock()  # For thread-safe operations on the heap
        self.new_patient_event = threading.Event()  # Event to signal when a new patient is added

    def push(self, patient):
        """
        Add a new patient to the priority queue and notify the ICU thread.
        """
        if patient.esi_priority is None:
            print(f"Patient {patient.name} does not have an assigned priority. Please calculate priority first.")
            return
        with self.lock:
            heapq.heappush(self.patients, patient)
        print(f"Patient {patient.name} with priority {patient.esi_priority} added to the queue.")

        # Signal that a new patient is added
        self.new_patient_event.set()

    def pop(self):
        """
        Remove and return the patient with the highest priority (lowest ESI value).
        """
        with self.lock:
            if not self.patients:
                print("No patients in the queue.")
                return None
            patient = heapq.heappop(self.patients)
        print(f"Patient {patient.name} with priority {patient.esi_priority} removed from the queue.")
        return patient

    def list_patients(self):
        """
        List all patients in the queue, ordered by priority.
        """
        with self.lock:
            if not self.patients:
                print("No patients in the queue.")
                return
            print("Patients in the queue (ordered by priority):")
            for patient in sorted(self.patients):
                print(f"{patient.name} (Priority: {patient.esi_priority})")

    def start_icu_consumer(self):
        """
        Start a separate thread for the ICU to process patients when new ones are added.
        """
        def icu_worker():
            while True:
                # Wait for a new patient to be added to the queue
                self.new_patient_event.wait()

                patient = self.pop()  # Get the highest-priority patient
                if patient:
                    operation_time = random.randint(1, 30)  # Random operation time
                    print(f"Operating on {patient.name} for {operation_time} seconds.")
                    time.sleep(operation_time)
                    print(f"Finished operating on {patient.name}.")
                else:
                    print("No patients to process. ICU is idle.")
                    time.sleep(5)  # Wait before checking again if no patients are present

                # Reset the event after processing one patient
                self.new_patient_event.clear()

        threading.Thread(target=icu_worker, daemon=True).start()
