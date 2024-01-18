# Real Estate Management Website

Welcome to the Real Estate Management Website! This project provides a platform for realtors to showcase their properties, allowing users to search for properties and express interest. The system includes separate dashboards for users, realtors, and administrators, each with specific functionalities.

## Features

- **User Registration and Authentication:**
  - Users, realtors, and administrators can register and log in securely.

- **User Dashboard:**
  - Users can view and search for properties.
  - Express interest or contact realtors for more information.

- **Realtor Dashboard:**
  - Realtors can add, edit, and manage their property listings.
  - Access to personal information editing and password change.

- **Admin Dashboard:**
  - Administrators have control over user and property management.
  - Manage registered users and properties efficiently.

- **Property Management:**
  - Realtors can add detailed property listings, including images.
  - Users can search and filter properties based on preferences.

## How to Run the Project

1. Clone the repository to your local machine.
   ```
   git clone https://github.com/your-username/real-estate-management.git
   ```

2. Install project dependencies.
   ```
   pip install -r requirements.txt
   ```

3. Set up the database.
   ```
   python manage.py makemigrations
   python manage.py migrate
   ```

4. Run the development server.
   ```
   python manage.py runserver
   ```

5. Access the application at `http://localhost:8000/` in your web browser.

## Additional Information

- This project uses Django for backend development.
- Feel free to explore and customize the project to suit your specific needs.
- For any issues or questions, please contact .
