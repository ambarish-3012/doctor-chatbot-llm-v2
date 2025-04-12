from database_connection import get_connection
from datetime import datetime

def list_doctors_by_department(department):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        query = """
        SELECT doctor_name, specialization
        FROM doctors
        WHERE department = %s
        """

        cursor.execute(query, (department,))
        rows = cursor.fetchall()
        cursor.close()
        conn.close()

        if not rows:
            return f"Sorry, no doctors found in the {department} department at the moment."

        doctors = [f"{row[0]} ({row[1]})" for row in rows]

        if len(doctors) == 1:
            return (
                f"There is only one doctor available in {department}:\n\n"
                f"- {doctors[0]}\n\n"
                f"Would you like to book an appointment with this doctor?"
            )
        else:
            return (
                f"Doctors in {department}:\n\n" +
                "\n".join(f"- {doc}" for doc in doctors) +
                "\n\nWhich doctor would you like to check availability for?"
            )

    except Exception as e:
        return f"Error retrieving doctors from {department}: {str(e)}"

def get_doctor_availability(doctor_name):
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        print(f"[Debug] Looking up availability for: {doctor_name}")

        query = """
            SELECT a.available_date, a.available_time
            FROM availability a
            JOIN doctors d ON a.doctor_id = d.doctor_id
            WHERE d.doctor_name = %s AND a.is_booked = 0 AND (a.available_date > CURDATE()
            OR (a.available_date = CURDATE() AND a.available_time > CURTIME()))
            ORDER BY a.available_date, a.available_time
        """
        cursor.execute(query, (doctor_name,))
        results = cursor.fetchall()
        cursor.close()
        conn.close()

        if not results:
            return f"No upcoming slots available for {doctor_name}."

        availability_list = [f"{row['available_date']} at {row['available_time']}" for row in results]
        return f"Available slots for {doctor_name}: {availability_list}"

    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print(f"[Error] Exception occurred:\n{error_details}")
        return f"An error occurred while checking availability for {doctor_name}.\nDetails: {e}"


def book_appointment(doctor_name, date, time):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        print(f"[Debug] Booking appointment with {doctor_name} on {date} at {time}")

        # Find doctor_id
        cursor.execute("SELECT doctor_id FROM doctors WHERE doctor_name = %s", (doctor_name,))
        result = cursor.fetchone()

        if result is None:
            return f"Doctor {doctor_name} not found."

        doctor_id = result[0]

        # Check if slot is available
        cursor.execute("""
            SELECT id FROM availability
            WHERE doctor_id = %s AND available_date = %s AND available_time = %s AND is_booked = 0
        """, (doctor_id, date, time))
        availability_result = cursor.fetchone()

        if availability_result is None:
            return f"The slot for Dr. {doctor_name} at {time} on {date} is not available."

        # Mark the slot as booked
        cursor.execute("""
            UPDATE availability
            SET is_booked = 1
            WHERE id = %s
        """, (availability_result[0],))
        conn.commit()
        cursor.close()
        conn.close()

        return f"Appointment confirmed with Dr. {doctor_name} on {date} at {time}."

    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print(f"[Error] Booking failed:\n{error_details}")
        return f"I'm sorry, there was a technical error while trying to book your appointment. Error details: {str(e)}"

