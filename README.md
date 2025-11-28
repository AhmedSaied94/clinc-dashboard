# Clinic Placement Dashboard

A modern, full-featured web application for managing and analyzing clinic placement data. Built with Django and featuring an intuitive dashboard with comprehensive analytics, data import capabilities, and user management.

## 📋 Table of Contents

- [Features](#features)
- [Screenshots](#screenshots)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Technologies Used](#technologies-used)
- [API Endpoints](#api-endpoints)
- [Deployment](#deployment)
- [Contributing](#contributing)
- [License](#license)

## ✨ Features

### 📊 Analytics Dashboard
- **Department Analytics**: Visualize placement distributions by department with interactive charts
- **Specialty Analytics**: Track placements by medical specialty with detailed breakdowns
- **Shift Analytics**: Monitor placement patterns across different shifts (AM, MD, PM, CLOSED)
- **Status Analytics**: Analyze full-time vs part-time placement statistics
- **Timeline Analytics**: View placement trends over time with date-based filtering

### 🏥 Placement Management
- **CRUD Operations**: Create, read, update, and delete placement records
- **Advanced Filtering**: Filter placements by date range, department, specialty, shift, and status
- **Bulk Import**: Import placements from Excel files with data validation
- **Template Download**: Download empty Excel templates for easy data entry
- **Replace Mode**: Option to replace all existing data during import
- **Search Functionality**: Quick search across all placement fields
- **Pagination**: Configurable rows per page (default: 10 rows)

### 👥 User Management
- **User CRUD**: Full user management for administrators
- **Role-Based Access**: Restrict user management to admin users only
- **User Profiles**: Personal profile management with password change functionality
- **Settings Page**: Customize theme preferences (light/dark mode) and notifications

### 🎨 User Interface
- **Modern Design**: Beautiful, responsive UI with gradient effects and smooth animations
- **Dark/Light Theme**: Toggle between light and dark themes with persistent preferences
- **Glassmorphism Effects**: Modern glass-style UI elements
- **Interactive Charts**: Chart.js powered visualizations with hover effects
- **Responsive Layout**: Mobile-friendly design that works on all devices
- **Bootstrap Icons**: Extensive use of icons for better UX

### 🔐 Security
- **Authentication Required**: All views protected with login requirements
- **Admin-Only Access**: User management restricted to superusers
- **Secure Forms**: CSRF protection on all forms
- **Session Management**: Secure session handling

## 🖼️ Screenshots

_Add screenshots of your dashboard here_

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment (recommended)

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/clinc_dashboard.git
cd clinc_dashboard
```

### Step 2: Create Virtual Environment

```bash
# Using venv
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Database Setup

```bash
# Run migrations
python manage.py migrate

# Create a superuser (optional, for admin access)
python manage.py createsuperuser
```

### Step 5: Collect Static Files

```bash
python manage.py collectstatic --noinput
```

### Step 6: Run Development Server

```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000/dashboard/` in your browser.

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the project root with the following variables:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=sqlite:///db.sqlite3
```

Or use Python `decouple` with default values as configured in `settings/base.py`.

### Settings Files

The project uses environment-specific settings:
- `settings/base.py`: Base settings for all environments
- `settings/dev.py`: Development settings
- `settings/production.py`: Production settings
- `settings/logging.py`: Logging configuration

## 📖 Usage

### Creating Your First Placement

1. Navigate to **Placements** → **Add New Placement**
2. Fill in the required fields:
   - Date
   - Shift (AM, MD, PM, or CLOSED)
   - Physician Name
   - Physician ID
   - Department
   - Specialty
   - Status (Full Time or Part Time)
   - Area (optional)
   - Room Number (optional)
3. Click **Save**

### Importing Placements from Excel

1. Navigate to **Placements** → **Import**
2. Click **Download Template** to get an empty Excel template
3. Fill in the template with your placement data
4. Upload the completed file
5. Optionally check **Replace existing data** to clear all current placements
6. Click **Import**

#### Excel Template Format

The Excel file should have the following columns:
- Date
- Shift
- Physician Name
- ID
- Department
- Speciality
- Status
- Area
- Room Number

### Using Analytics

1. Navigate to any analytics page from the sidebar
2. Use the filter panel to narrow down results:
   - Select date ranges
   - Filter by department, specialty, shift, or status
3. View interactive charts and statistics
4. Export data if needed

### Managing Users (Admin Only)

1. Log in as a superuser
2. Navigate to **Users** in the sidebar
3. Create, edit, or delete user accounts
4. Assign staff or superuser privileges

### Management Commands

Import placements via command line:

```bash
python manage.py import_placements --file path/to/file.xlsx --replace
```

## 📁 Project Structure

```
clinc_dashboard/
├── clinic_dashboard/          # Main project directory
│   ├── settings/              # Environment-specific settings
│   │   ├── base.py           # Base settings
│   │   ├── dev.py            # Development settings
│   │   └── production.py     # Production settings
│   ├── urls.py               # Root URL configuration
│   └── wsgi.py               # WSGI configuration
├── dashboard/                 # Main dashboard app
│   ├── analytics_views.py    # Analytics page views
│   ├── forms.py              # Form definitions
│   ├── urls.py               # Dashboard URL patterns
│   ├── views.py              # Main views (CRUD, import, etc.)
│   ├── templatetags/         # Custom template tags
│   ├── templates/            # HTML templates
│   │   ├── base.html
│   │   ├── components/       # Reusable components
│   │   └── dashboard/        # Dashboard templates
│   └── static/               # Static files (CSS, JS, images)
├── placements/               # Placement app
│   ├── models.py             # Placement model
│   ├── management/
│   │   └── commands/
│   │       └── import_placements.py  # Import command
│   └── migrations/           # Database migrations
├── static/                   # Global static files
│   ├── css/
│   │   ├── dashboard.css
│   │   ├── theme.css
│   │   ├── navbar.css
│   │   └── sidebar.css
│   └── js/
│       ├── dashboard.js
│       ├── charts.js
│       ├── theme.js
│       └── sidebar.js
├── manage.py                 # Django management script
├── requirements.txt          # Python dependencies
├── db.sqlite3                # SQLite database (development)
└── README.md                 # This file
```

## 🛠️ Technologies Used

### Backend
- **Django 5.0+**: Web framework
- **Python 3.8+**: Programming language
- **Pandas**: Data processing and Excel file handling
- **OpenPyXL**: Excel file reading/writing

### Frontend
- **Bootstrap 5**: CSS framework
- **Bootstrap Icons**: Icon library
- **Chart.js**: Interactive charts and graphs
- **GSAP**: Animation library
- **Crispy Forms**: Enhanced Django forms
- **Custom CSS**: Theme system with CSS variables

### Database
- **SQLite**: Default database (development)
- **PostgreSQL/MySQL**: Recommended for production

## 🔌 API Endpoints

### Analytics API

**GET** `/dashboard/api/analytics/`

Returns analytics data as JSON. Accepts query parameters:
- `type`: Analytics type (department, specialty, shift, status, timeline)
- `start_date`: Start date filter (YYYY-MM-DD)
- `end_date`: End date filter (YYYY-MM-DD)
- `department`: Department filter
- `specialty`: Specialty filter
- `shift`: Shift filter
- `status`: Status filter

**Example:**
```bash
GET /dashboard/api/analytics/?type=department&start_date=2024-01-01
```

## 🚀 Deployment

### Production Deployment

For detailed deployment instructions, see [DEPLOYMENT.md](DEPLOYMENT.md).

#### Quick Steps:

1. Set environment variables
2. Configure `ALLOWED_HOSTS` in settings
3. Set `DEBUG=False`
4. Use a production database (PostgreSQL recommended)
5. Configure static file serving
6. Set up a production WSGI server (Gunicorn)

### Docker Deployment (Optional)

```bash
docker build -t clinic-dashboard .
docker run -p 8000:8000 clinic-dashboard
```

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Code Style

- Follow PEP 8 for Python code
- Use meaningful variable and function names
- Add docstrings to classes and functions
- Write tests for new features

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👤 Author

**Ahmed Saied**

- GitHub: [@AhmedSaied94](https://github.com/AhmedSaied94)

## 🙏 Acknowledgments

- Django community for excellent documentation
- Bootstrap team for the UI framework
- Chart.js for amazing chart library
- All contributors and users of this project

## 📞 Support

For support, email your-email@example.com or open an issue in the GitHub repository.

## 🔄 Changelog

### Version 1.0.0
- Initial release
- Placement CRUD operations
- Analytics dashboard
- Excel import functionality
- User management
- Theme switching (light/dark mode)
- Responsive design

---

**Made with ❤️ using Django and Bootstrap**

