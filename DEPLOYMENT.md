# PythonAnywhere Deployment Guide for Clinic Dashboard

Complete step-by-step guide to deploy your Clinic Placement Dashboard to PythonAnywhere.

**Your Username:** `AhmedSaied94`  
**Repository:** `git@github.com-AhmedSaied94:AhmedSaied94/clinc-dashboard.git`  
**Your Domain:** `ahmedsaied94.pythonanywhere.com`

---

## 📋 Prerequisites

- ✅ PythonAnywhere account (free tier works, but paid recommended for production)
- ✅ SSH access configured (for git clone) or Git credentials
- ✅ Your GitHub repository cloned locally or accessible

---

## 🚀 Step-by-Step Deployment

### Step 1: Access PythonAnywhere Console

1. Log in to [PythonAnywhere](https://www.pythonanywhere.com/)
2. Go to the **Dashboard**
3. Click on **Bash** (or open a console)

---

### Step 2: Clone Your Repository

In the Bash console, run:

```bash
cd /home/AhmedSaied94
git clone git@github.com-AhmedSaied94:AhmedSaied94/clinc-dashboard.git
cd clinc_dashboard
```

**Note:** If SSH isn't configured, use HTTPS:

```bash
git clone https://github.com/AhmedSaied94/clinc-dashboard.git
cd clinc_dashboard
```

---

### Step 3: Create Virtual Environment

Choose one of these methods:

#### Option A: Using `venv` (Standard method - Recommended)

```bash
cd /home/AhmedSaied94/clinc_dashboard
python3.12 -m venv venv
source venv/bin/activate
```

**Verify virtualenv is active** (you should see `(venv)` in your prompt)

#### Option B: Using `mkvirtualenv` (Alternative)

```bash
# If virtualenvwrapper is installed
mkvirtualenv --python=/usr/bin/python3.12 clinc_dashboard
```

After creating, activate it:

```bash
workon clinc_dashboard
```

**Verify virtualenv is active** (you should see `(clinc_dashboard)` in your prompt)

---

### Step 4: Install Dependencies

Make sure your virtualenv is activated, then:

```bash
cd /home/AhmedSaied94/clinc_dashboard
pip install --upgrade pip
pip install -r requirements.txt
```

**Expected packages:**

- Django>=5.0
- pandas>=2.0.0
- openpyxl>=3.1.0
- django-crispy-forms>=2.0
- crispy-bootstrap5>=0.7
- python-decouple>=3.8
- gunicorn>=21.0.0

---

### Step 5: Configure Environment Variables

1. **Create `.env` file from template:**

```bash
cp .env.production .env
nano .env
```

2. **Set the following variables:**

```env
SECRET_KEY=your-super-secret-key-here-generate-a-new-one
DEBUG=False
ALLOWED_HOSTS=ahmedsaied94.pythonanywhere.com
```

3. **Generate a new SECRET_KEY:**

In a Python console:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Copy the output and paste it as your `SECRET_KEY` value.

4. **Save and exit** (Ctrl+X, then Y, then Enter)

**Important:** Never commit the `.env` file to Git!

---

### Step 6: Run Database Migrations

```bash
cd /home/AhmedSaied94/clinc_dashboard
python manage.py migrate --settings=clinic_dashboard.settings.production
```

This creates the database tables in `db.sqlite3`.

---

### Step 7: Create Superuser

```bash
python manage.py createsuperuser --settings=clinic_dashboard.settings.production
```

Follow the prompts to create your admin account.

---

### Step 8: Collect Static Files

**Important:** Make sure your virtualenv is activated before running this command.

```bash
cd /home/AhmedSaied94/clinc_dashboard
source venv/bin/activate  # or: workon clinc_dashboard if using mkvirtualenv
python manage.py collectstatic --settings=clinic_dashboard.settings.production --noinput
```

This collects all static files (including Django admin files) into the `staticfiles/` directory.

**Verify admin files were collected:**

```bash
ls -la /home/AhmedSaied94/clinc_dashboard/staticfiles/admin/
```

You should see CSS, JS, and other admin static files in this directory.

---

### Step 9: Create Media Directory (if needed)

```bash
mkdir -p /home/AhmedSaied94/clinc_dashboard/media
```

---

### Step 10: Create Web App in PythonAnywhere

1. Go to the **Web** tab in PythonAnywhere dashboard
2. Click **"Add a new web app"**
3. Choose **"Manual configuration"** (NOT the Django wizard)
4. Select **Python 3.12** (or latest available)

---

### Step 11: Configure WSGI File

1. In the **Web** tab, click on the **WSGI configuration file** link
2. **Delete all existing content**
3. Copy and paste this content:

```python
# +++++++++++ DJANGO +++++++++++
import os
import sys

# Add your project directory to the sys.path
path = '/home/AhmedSaied94/clinc_dashboard'
if path not in sys.path:
    sys.path.insert(0, path)

# Set environment variable for production settings
os.environ['DJANGO_SETTINGS_MODULE'] = 'clinic_dashboard.settings.production'

# Activate virtualenv (choose the method you used)

# If using venv (standard virtualenv in project root):
activate_this = '/home/AhmedSaied94/clinc_dashboard/venv/bin/activate_this.py'
if os.path.exists(activate_this):
    with open(activate_this) as f:
        exec(f.read(), {'__file__': activate_this})

# OR if using mkvirtualenv:
# activate_this = '/home/AhmedSaied94/.virtualenvs/clinc_dashboard/bin/activate_this.py'
# if os.path.exists(activate_this):
#     with open(activate_this) as f:
#         exec(f.read(), {'__file__': activate_this})

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

4. **The default configuration uses `venv`** (virtualenv in project root). If you used `mkvirtualenv`, uncomment that block and comment out the venv block instead.
5. Click **Save**

---

### Step 12: Configure Web App Settings

In the **Web** tab, scroll down to configure:

#### Source code

```text
/home/AhmedSaied94/clinc_dashboard
```

#### Working directory

```text
/home/AhmedSaied94/clinc_dashboard
```

#### Virtualenv

**If you used `venv` (standard virtualenv in project root):**

```text
/home/AhmedSaied94/clinc_dashboard/venv
```

**If you used `mkvirtualenv`:**

```text
/home/AhmedSaied94/.virtualenvs/clinc_dashboard
```

#### Static files mapping

Add these mappings in the **Static files** section:

| URL          | Directory                                          |
|--------------|----------------------------------------------------|
| `/static/`   | `/home/AhmedSaied94/clinc_dashboard/staticfiles` |
| `/media/`    | `/home/AhmedSaied94/clinc_dashboard/media`       |

**Important Notes:**

- The `/static/` URL must map to the `staticfiles` directory (where `collectstatic` puts files)
- Make sure there's **NO trailing slash** in the directory path
- After adding mappings, click **Save**

**Verify static files after collection:**

```bash
# Check admin files were collected
ls -la /home/AhmedSaied94/clinc_dashboard/staticfiles/admin/
```

You should see folders like `css/`, `js/`, `img/` inside the admin directory.

---

### Step 13: Reload Web App

1. Scroll to the top of the **Web** tab
2. Click the green **Reload** button
3. Wait for the reload to complete (usually 10-30 seconds)

---

### Step 14: Test Your Application

Visit your site:

- **Main Dashboard:** <https://ahmedsaied94.pythonanywhere.com/dashboard/>
- **Login Page:** <https://ahmedsaied94.pythonanywhere.com/dashboard/login/>
- **Admin Panel:** <https://ahmedsaied94.pythonanywhere.com/admin/>

---

## 🔧 Troubleshooting

### Check Error Logs

1. In the **Web** tab, click **"Error log"** link
2. Scroll to the bottom to see recent errors
3. Look for import errors, database errors, or configuration issues

### Common Issues and Solutions

#### 1. Import Error: No module named 'django'

**Problem:** Virtualenv not properly activated in WSGI file.

**Solution:**

- Check the virtualenv path in WSGI file matches your setup
- Ensure the virtualenv activation block is uncommented
- Verify virtualenv exists: `ls -la /home/AhmedSaied94/.virtualenvs/clinc_dashboard`

#### 2. Static Files Not Loading (404 errors) / Admin Static Files Missing

**Problem:** Static files not collected or mapping incorrect, especially admin files.

**Solution:**

```bash
cd /home/AhmedSaied94/clinc_dashboard
source venv/bin/activate  # or: workon clinc_dashboard if using mkvirtualenv
python manage.py collectstatic --settings=clinic_dashboard.settings.production --noinput
```

**For admin static files specifically:**

```bash
# Verify admin files exist
ls -la /home/AhmedSaied94/clinc_dashboard/staticfiles/admin/

# If admin folder is missing or incomplete, force re-collection
rm -rf /home/AhmedSaied94/clinc_dashboard/staticfiles
python manage.py collectstatic --settings=clinic_dashboard.settings.production --noinput --clear
```

**Verification steps:**

- Verify static files mapping in Web tab: `/static/` → `/home/AhmedSaied94/clinc_dashboard/staticfiles`
- Check that `staticfiles/admin/` directory exists and contains CSS/JS files
- Ensure no trailing slash in directory path in PythonAnywhere settings
- Test admin page: `https://ahmedsaied94.pythonanywhere.com/admin/`

#### 3. 500 Internal Server Error

**Problem:** Usually configuration or database issue.

**Solution:**

- Check error log for specific error message
- Temporarily enable DEBUG to see detailed errors:

  ```bash
  nano .env
  # Change: DEBUG=True
  # Reload web app
  ```

- **Remember to set DEBUG=False again after fixing!**

#### 4. Database Errors

**Problem:** Database file permissions or missing migrations.

**Solution:**

```bash
# Fix permissions
chmod 664 /home/AhmedSaied94/clinc_dashboard/db.sqlite3
chmod 775 /home/AhmedSaied94/clinc_dashboard

# Re-run migrations
python manage.py migrate --settings=clinic_dashboard.settings.production
```

#### 5. ModuleNotFoundError for project modules

**Problem:** Python path not set correctly in WSGI.

**Solution:**

- Verify the path in WSGI file is correct: `/home/AhmedSaied94/clinc_dashboard`
- Check that `clinic_dashboard` directory exists in that path

#### 6. CSRF Verification Failed

**Problem:** ALLOWED_HOSTS not configured correctly.

**Solution:**

- Check `.env` file has: `ALLOWED_HOSTS=ahmedsaied94.pythonanywhere.com`
- Reload web app after changing

### Enable DEBUG Temporarily (For Troubleshooting Only)

**⚠️ WARNING: Only for debugging, never in production!**

```bash
nano /home/AhmedSaied94/clinc_dashboard/.env
```

Change:

```env
DEBUG=True
```

Then reload web app. **Set it back to `False` immediately after fixing!**

### Test Django Setup from Console

```bash
cd /home/AhmedSaied94/clinc_dashboard
source ~/.virtualenvs/clinc_dashboard/bin/activate  # or: source venv/bin/activate

# Check for configuration errors
python manage.py check --settings=clinic_dashboard.settings.production

# Test database connection
python manage.py dbshell --settings=clinic_dashboard.settings.production
```

---

## 📦 Updating Your Application

When you push new changes to GitHub:

```bash
cd /home/AhmedSaied94/clinc_dashboard

# Pull latest changes
git pull origin main

# Activate virtualenv
source ~/.virtualenvs/clinc_dashboard/bin/activate  # or: source venv/bin/activate

# Install any new dependencies
pip install -r requirements.txt

# Run new migrations (if any)
python manage.py migrate --settings=clinic_dashboard.settings.production

# Collect static files (if CSS/JS changed)
source venv/bin/activate  # or: workon clinc_dashboard if using mkvirtualenv
python manage.py collectstatic --settings=clinic_dashboard.settings.production --noinput

# If admin files are missing, use --clear flag
# python manage.py collectstatic --settings=clinic_dashboard.settings.production --noinput --clear
```

Then **reload the web app** from the **Web** tab.

---

## 🔒 Security Best Practices

1. **Never commit `.env` file** - It contains sensitive information
2. **Use strong SECRET_KEY** - Generate a new one for production
3. **Keep DEBUG=False** in production - Never enable in production
4. **Regular backups** - Backup `db.sqlite3` regularly
5. **Update dependencies** - Keep Django and packages updated
6. **Monitor error logs** - Check for suspicious activity

---

## 💾 Database Backups

### Manual Backup

```bash
# Create timestamped backup
cp /home/AhmedSaied94/clinc_dashboard/db.sqlite3 \
   /home/AhmedSaied94/clinc_dashboard/db.sqlite3.backup-$(date +%Y%m%d-%H%M%S)
```

### Download Backup

1. Go to **Files** tab in PythonAnywhere
2. Navigate to `/home/AhmedSaied94/clinc_dashboard/`
3. Download `db.sqlite3`
4. Store it securely

### Automated Backups (Optional)

Create a scheduled task in **Tasks** tab:

```bash
0 2 * * * cp /home/AhmedSaied94/clinc_dashboard/db.sqlite3 /home/AhmedSaied94/backups/db-$(date +\%Y\%m\%d).sqlite3
```

(Runs daily at 2 AM)

---

## 📊 Post-Deployment Checklist

- [ ] Application loads without errors
- [ ] Can log in with superuser account
- [ ] Static files (CSS, JS, images) load correctly
- [ ] Dashboard pages are accessible
- [ ] Analytics pages work correctly
- [ ] Can create/edit placements
- [ ] Excel import functionality works
- [ ] Database operations work
- [ ] Error logs are clean
- [ ] DEBUG is set to False
- [ ] `.env` file is not in Git
- [ ] Database backup created

---

## 🔗 Your Application URLs

After successful deployment:

| Page | URL |
|------|-----|
| **Dashboard Home** | <https://ahmedsaied94.pythonanywhere.com/dashboard/> |
| **Login** | <https://ahmedsaied94.pythonanywhere.com/dashboard/login/> |
| **Placements List** | <https://ahmedsaied94.pythonanywhere.com/dashboard/placements/> |
| **Department Analytics** | <https://ahmedsaied94.pythonanywhere.com/dashboard/analytics/department/> |
| **Admin Panel** | <https://ahmedsaied94.pythonanywhere.com/admin/> |

---

## 📚 Additional Resources

- **PythonAnywhere Help:** <https://help.pythonanywhere.com/>
- **Django Deployment Guide:** <https://docs.djangoproject.com/en/5.2/howto/deployment/>
- **Django Static Files:** <https://docs.djangoproject.com/en/5.2/howto/static-files/>
- **PythonAnywhere Web App Guide:** <https://help.pythonanywhere.com/pages/DeployExistingDjangoProject/>

---

## 🆘 Getting Help

If you encounter issues:

1. Check the **Error log** in PythonAnywhere Web tab
2. Review this guide's troubleshooting section
3. Check Django documentation
4. PythonAnywhere community forums
5. Create an issue in your GitHub repository

---

## 📝 Notes

- Free PythonAnywhere accounts have limitations (CPU time, web app reloads per day)
- Consider upgrading for production use
- SQLite works fine for small to medium applications
- For larger scale, consider PostgreSQL (available on paid plans)

---

### Version Information

- **Last Updated:** 2025-01-XX  
- **Django Version:** 5.0+  
- **Python Version:** 3.12

---

**Happy Deploying! 🚀**
