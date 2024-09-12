import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import tkinter as tk
from tkinter import messagebox

# Email details
smtp_server = 'smtp.gmail.com'  # Example: 'smtp.gmail.com' for Gmail
smtp_port = 587
sender_email = 'Yousef9amr@gmail.com'  # Your email
sender_password = 'vqgs jgpn aels krgj'

recipient_list = []
first_names = []

def send_emails():
    body = body_text.get("1.0", tk.END).strip()  # Get the body from the large text box
    subject = subject_entry.get().strip()  # Get the subject from the subject entry box

    print("Send Emails function triggered...")  # Debugging statement

    if not recipient_list or not first_names or not body or not subject:
        messagebox.showerror("Error", "Please fill in all fields: recipients, names, subject, and body.")
        return

    try:
        print("Attempting to connect to the SMTP server...")  # Debugging statement
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)

        for recipient_email, first_name in zip(recipient_list, first_names):
            personalized_body = f"Dear Doctor {first_name},\n\n{body}"
            print(f"Sending email to {recipient_email}...")  # Debugging statement

            # Create email
            message = MIMEMultipart()
            message['From'] = sender_email
            message['To'] = recipient_email
            message['Subject'] = subject
            message.attach(MIMEText(personalized_body, 'plain'))

            # Send the email
            server.sendmail(sender_email, recipient_email, message.as_string())

        server.quit()
        messagebox.showinfo("Success", "Emails sent successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to send emails: {str(e)}")

# Function to add email to the recipient list
def add_email():
    email = email_entry.get().strip()
    if email:
        recipient_list.append(email)
        email_listbox.insert(tk.END, email)
        email_entry.delete(0, tk.END)
        print(f"Added email: {email}")  # Debugging statement
    else:
        messagebox.showerror("Error", "Please enter a valid email.")

# Function to remove selected email
def delete_email():
    selected_email = email_listbox.curselection()
    if selected_email:
        index = selected_email[0]
        recipient_list.pop(index)
        email_listbox.delete(index)
        print(f"Deleted email at index {index}")  # Debugging statement
    else:
        messagebox.showerror("Error", "Please select an email to delete.")

# Function to add name to the first name list
def add_name():
    name = name_entry.get().strip()
    if name:
        first_names.append(name)
        name_listbox.insert(tk.END, name)
        name_entry.delete(0, tk.END)
        print(f"Added name: {name}")  # Debugging statement
    else:
        messagebox.showerror("Error", "Please enter a valid name.")

# Function to remove selected name
def delete_name():
    selected_name = name_listbox.curselection()
    if selected_name:
        index = selected_name[0]
        first_names.pop(index)
        name_listbox.delete(index)
        print(f"Deleted name at index {index}")  # Debugging statement
    else:
        messagebox.showerror("Error", "Please select a name to delete.")

# Create GUI window
root = tk.Tk()
root.title("Email Sender")

# Email Section
tk.Label(root, text="Emails:").grid(row=0, column=0, padx=10, pady=5)
email_entry = tk.Entry(root, width=40)
email_entry.grid(row=0, column=1, padx=10, pady=5)
add_email_button = tk.Button(root, text="Add Email", command=add_email)
add_email_button.grid(row=0, column=2, padx=10, pady=5)

# Listbox to display added emails
email_listbox = tk.Listbox(root, width=40, height=5)
email_listbox.grid(row=1, column=1, padx=10, pady=5)
delete_email_button = tk.Button(root, text="Delete Email", command=delete_email)
delete_email_button.grid(row=1, column=2, padx=10, pady=5)

# Name Section
tk.Label(root, text="First Names:").grid(row=2, column=0, padx=10, pady=5)
name_entry = tk.Entry(root, width=40)
name_entry.grid(row=2, column=1, padx=10, pady=5)
add_name_button = tk.Button(root, text="Add Name", command=add_name)
add_name_button.grid(row=2, column=2, padx=10, pady=5)

# Listbox to display added names
name_listbox = tk.Listbox(root, width=40, height=5)
name_listbox.grid(row=3, column=1, padx=10, pady=5)
delete_name_button = tk.Button(root, text="Delete Name", command=delete_name)
delete_name_button.grid(row=3, column=2, padx=10, pady=5)

# Subject Section
tk.Label(root, text="Email Subject:").grid(row=4, column=0, padx=10, pady=5)
subject_entry = tk.Entry(root, width=40)
subject_entry.grid(row=4, column=1, padx=10, pady=5)

# Body Section
tk.Label(root, text="Email Body:").grid(row=5, column=0, padx=10, pady=5)
body_text = tk.Text(root, width=40, height=10)
body_text.grid(row=5, column=1, padx=10, pady=5)

# Submit Button
submit_button = tk.Button(root, text="Submit", command=send_emails)
submit_button.grid(row=6, column=1, pady=20)

# Run the GUI loop
root.mainloop()