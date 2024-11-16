from patient_library import Patient, PatientManager

def main():
    manager = PatientManager()
    manager.start_icu_consumer()  # Start ICU consumer thread

    while True:
        print("\nOptions:")
        print("1. Add a new patient")
        print("2. View all patients")
        print("3. Remove highest-priority patient")
        print("4. Exit")

        choice = input("Enter your choice (1-4): ").strip()
        if choice == "1":
            # Create a new patient
            patient_name = input("Enter the patient's name: ").strip()
            try:
                patient_age = int(input("Enter the patient's age: "))
            except ValueError:
                print("Invalid input. Age must be a number.")
                continue
            patient_sex = input("Enter the patient's sex (Male/Female): ").strip()

            patient = Patient(patient_name, patient_age, patient_sex)
            patient.calculate_esi_priority()

            # Add the patient to the manager
            manager.push(patient)

        elif choice == "2":
            # List all patients
            manager.list_patients()

        elif choice == "3":
            # Remove highest-priority patient
            manager.pop()

        elif choice == "4":
            print("Exiting...")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
