# 📝 MyBlog - A Simple Blog Website

Welcome to **MyBlog**, a web application where users can read, write, and share blog posts. Built with Django (Python), this blog platform offers a clean UI, CRUD features, and a user-friendly interface.



---

## 🚀 Features

- 🖊️ Create, edit, and delete blog posts
- 🌐 Responsive frontend design (Bootstrap/Tailwind)
- 🔍 Search functionality (optional)
- 📆 Post date & time display


## In Future

- 🗂️ Blog post categorization (optional)
- 🧾 Commenting system (optional)
- ❤️ Like / Dislike System – Enable reactions on posts and comments.
- 🌙 Dark Mode Toggle – Theme switch for better UX.
- 📤 Social Share Buttons – Share posts via WhatsApp, Facebook, X (Twitter), etc.

## 🛠️ Tech Stack

- **Frontend**: HTML, CSS, Bootstrap
- **Backend**: Django (Python)
- **Database**: SQLite 
- **Authentication**: Django Admin 

---

## 🏁 How to Run Locally

```bash
# Clone the repository
git clone [https://github.com/yourusername/blogwebsite.git](https://github.com/Dilnavazsida/Blog_website.git)

# Navigate to the project directory
cd Blog_website\blog\blog

# Create virtual environment and activate
python -m venv venv
# On Windows: venv\Scripts\activate

# Run migrations
python manage.py migrate

# Start the server
python manage.py runserver

# Open in browser
http://127.0.0.1:8000/
