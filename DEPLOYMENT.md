# PythonAnywhere Deployment Guide for Clinic Dashboard

## Prerequisites
- PythonAnywhere account (free or paid)
- Git repository with your code (or zip file to upload)
- Your username: **AhmedSaied94**

## Step 1: Upload Your Code

### Option A: Using Git (Recommended)
1. Go to PythonAnywhere dashboard
2. Open a Bash console
3. Clone your repository:
   ```bash
   git clone https://github.com/yourusername/clinc_dashboard.git
   cd clinc_dashboard
   ```

### Option B: Upload Files
1. Use the "Files" tab in PythonAnywhere dashboard
2. Upload your project as a zip file
3. Extract it to `/home/AhmedSaied94/clinc_dashboard`

## Step 2: Create Virtual Environment

In the Bash console:
```bash
cd /home/AhmedSaied94/clinc_dashboard
mkvirtualenv --python=/usr/bin/python3.12 clinc_dashboard
```

Or using virtualenv:
```bash
python3.12 -m venv venv
source venv/bin/activate
```

## Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

## Step 4: Configure Environment Variables

1. Copy the production environment template:
   ```bash
   cp .env.production .env
   ```

2. Edit the `.env` file:
   ```bash
   nano .env
   ```

3. Update these values:
   - `SECRET_KEY`: Generate a new secret key using:
     ```python
     python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
     ```
   - `ALLOWED_HOSTS`: Should already be set to `ahmedsaied94.pythonanywhere.com`
   - Email settings (if needed)

## Step 5: Collect Static Files

```bash
python manage.py collectstatic --settings=clinic_dashboard.settings.production --noinput
```

## Step 6: Setup Database

Since we're using SQLite, either:

### Option A: Copy existing database
Upload your `db.sqlite3` file to `/home/AhmedSaied94/clinc_dashboard/`

### Option B: Create fresh database
```bash
python manage.py migrate --settings=clinic_dashboard.settings.production
python manage.py createsuperuser --settings=clinic_dashboard.settings.production
```

## Step 7: Create Web App

1. Go to PythonAnywhere **Web** tab
2. Click "Add a new web app"
3. Choose "Manual configuration" (not Django wizard)
4. Select Python 3.12

## Step 8: Configure WSGI File

1. In the **Web** tab, click on the WSGI configuration file link
2. Delete all content and replace with the content from `pythonanywhere_wsgi.py`
3. Update the virtualenv path if needed (see Step 9)

## Step 9: Configure Web App Settings

In the **Web** tab, configure:

### Source code:
```
/home/AhmedSaied94/clinc_dashboard
```

### Working directory:
```
/home/AhmedSaied94/clinc_dashboard
```

### Virtualenv:
If you used `mkvirtualenv`:
```
/home/AhmedSaied94/.virtualenvs/clinc_dashboard
```

If you used `venv`:
```
/home/AhmedSaied94/clinc_dashboard/venv
```

### Static files mapping:

| URL          | Directory                                          |
|--------------|----------------------------------------------------|
| /static/     | /home/AhmedSaied94/clinc_dashboard/staticfiles     |
| /media/      | /home/AhmedSaied94/clinc_dashboard/media           |

## Step 10: Create Media Directory

```bash
mkdir -p /home/AhmedSaied94/clinc_dashboard/media
```

## Step 11: Reload Web App

1. Go to **Web** tab
2. Click the green **Reload** button
3. Wait for reload to complete

## Step 12: Test Your Application

Visit: `https://ahmedsaied94.pythonanywhere.com`

### Check admin panel:
`https://ahmedsaied94.pythonanywhere.com/admin/`

## Troubleshooting

### Check Error Logs
In the **Web** tab:
- Click on "Error log" link to view errors
- Click on "Server log" link to view access logs

### Common Issues:

1. **Import errors**: Check virtual environment is activated in WSGI file
2. **Static files not loading**: Verify static files mapping and run collectstatic
3. **500 errors**: Check error log, usually DEBUG=False hides error details
4. **Database errors**: Ensure db.sqlite3 has correct permissions

### Enable DEBUG temporarily (for troubleshooting only):
Edit `.env`:
```
DEBUG=True
```
Then reload the web app. **Remember to set it back to False!**

### View detailed errors in console:
```bash
cd /home/AhmedSaied94/clinc_dashboard
source ~/.virtualenvs/clinc_dashboard/bin/activate
python manage.py check --settings=clinic_dashboard.settings.production
```

## Post-Deployment Tasks

1. Create superuser if you haven't:
   ```bash
   python manage.py createsuperuser --settings=clinic_dashboard.settings.production
   ```

2. Load any initial data:
   ```bash
   python manage.py loaddata your_fixture.json --settings=clinic_dashboard.settings.production
   ```

3. Set up scheduled tasks (if needed):
   - Go to **Tasks** tab in PythonAnywhere
   - Add any management commands that need to run periodically

## Updating Your Application

When you make changes:

```bash
cd /home/AhmedSaied94/clinc_dashboard
git pull  # if using git

# Activate virtualenv
source ~/.virtualenvs/clinc_dashboard/bin/activate

# Install any new dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate --settings=clinic_dashboard.settings.production

# Collect static files
python manage.py collectstatic --settings=clinic_dashboard.settings.production --noinput
```

Then reload the web app from the **Web** tab.

## Security Notes

1. Keep your `.env` file secure - never commit it to git
2. Use strong SECRET_KEY in production
3. Regularly backup your database
4. Monitor error logs for security issues
5. Keep Django and dependencies updated

## Database Backups

Download your database regularly:
1. Go to **Files** tab
2. Navigate to `/home/AhmedSaied94/clinc_dashboard/`
3. Download `db.sqlite3`

Or use console:
```bash
cp db.sqlite3 db.sqlite3.backup-$(date +%Y%m%d)
```

## Support

- PythonAnywhere Help: https://help.pythonanywhere.com/
- Django Deployment Docs: https://docs.djangoproject.com/en/5.2/howto/deployment/

## Your Application URLs

- Main site: https://ahmedsaied94.pythonanywhere.com
- Admin panel: https://ahmedsaied94.pythonanywhere.com/admin/
- Dashboard: https://ahmedsaied94.pythonanywhere.com/dashboard/
