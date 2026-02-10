# Supabase Integration Guide

This guide explains how to set up Supabase for use with the Lecture Note Sharing Platform. Supabase provides both a managed PostgreSQL database and cloud file storage, making it ideal for Vercel deployments.

## Overview

The LNSP now supports three database options:
1. **SQLite** (default, local development)
2. **MySQL** (optional, self-hosted or managed)
3. **PostgreSQL via Supabase** (recommended for production/Vercel)

For file uploads/downloads:
- **Local filesystem** (default, development only)
- **Supabase Storage** (recommended for production)

## Supabase Free Tier Benefits

- **500 MB database** (PostgreSQL)
- **1 GB file storage**
- **Up to 500,000 monthly active users**
- **No credit card required** for free tier
- **Automatic backups** and **SSL encryption**

## Step 1: Create a Supabase Project

1. Go to [https://supabase.com](https://supabase.com)
2. Click **"Start your project"** or sign in if you have an account
3. Create a new project:
   - **Project Name**: e.g., "LNSP" or "Lecture-Note-Platform"
   - **Database Password**: Create a strong password (save this!)
   - **Region**: Choose closest to your users
   - Click **"Create new project"**

4. Wait for the project to initialize (2-5 minutes)

## Step 2: Get Your Database Credentials

1. In the Supabase dashboard, click your project
2. Go to **Settings > Database**
3. Note the following information:
   - **Host**: `db.xxxxx.supabase.co` (from Connection Pooler or Direct Connection)
   - **Port**: `5432` (standard PostgreSQL)
   - **Database**: `postgres`
   - **Username**: `postgres`
   - **Password**: The password you created during project setup

4. Construct your `DATABASE_URL`:
   ```
   postgresql://postgres:<password>@db.<project-id>.supabase.co:5432/postgres
   ```

## Step 3: Create a Storage Bucket

1. In the Supabase dashboard, go to **Storage**
2. Click **"Create a new bucket"**
3. **Bucket name**: `lecture-notes`
4. **Public bucket**: Toggle **ON** (so files can be downloaded without authentication)
5. Click **"Create bucket"**

6. Click on the `lecture-notes` bucket, then **Bucket Settings**
7. Copy the **Bucket URL** (or construct it: `https://project-id.supabase.co/storage/v1/object/public/lecture-notes`)

## Step 4: Get Your Supabase API Keys

1. Go to **Settings > API**
2. Under **Project API keys**, you'll see:
   - **Project URL**: `https://xxxxx.supabase.co`
   - **anon (public)**: Use this for `SUPABASE_KEY`
   - **service_role (secret)**: Use this for `SUPABASE_SERVICE_KEY` (keep secret!)

## Step 5: Configure Local Environment

1. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` with your Supabase credentials:
   ```env
   # Use PostgreSQL via Supabase
   DB_CONNECTION=postgres

   # Your Supabase database URL
   DATABASE_URL=postgresql://postgres:your-password@db.xxxx.supabase.co:5432/postgres

   # Supabase Storage credentials
   SUPABASE_URL=https://xxxxx.supabase.co
   SUPABASE_KEY=your-anon-key
   SUPABASE_SERVICE_KEY=your-service-role-key
   SUPABASE_BUCKET_NAME=lecture-notes

   # Flask secret key (generate a new one for production)
   SECRET_KEY=your-secret-key-here
   ```

## Step 6: Install Dependencies

If you haven't already, install the new packages:

```bash
pip install -r requirements.txt
```

This includes:
- `supabase` - Supabase Python client
- `psycopg2-binary` - PostgreSQL driver

## Step 7: Initialize the Database

Run the database initialization script:

```bash
python init_db.py
```

This will:
1. Detect that you're using PostgreSQL
2. Create the necessary tables in Supabase PostgreSQL
3. Display the connection status

## Step 8: Test Locally

1. Start the Flask application:
   ```bash
   python run.py
   ```

2. Open http://localhost:5000 in your browser
3. Register a new account
4. Test uploading a file (should upload to Supabase Storage)
5. Test downloading a file as a student

## Deploying to Vercel

### Prerequisites
- A Vercel account (free at [vercel.com](https://vercel.com))
- Your project on GitHub

### Steps

1. **Push your code to GitHub**:
   ```bash
   git add .
   git commit -m "Add Supabase integration for Vercel deployment"
   git push origin main
   ```

2. **Connect to Vercel**:
   - Go to [vercel.com](https://vercel.com)
   - Click **"Add New Project"**
   - Select your GitHub repository
   - Click **"Import"**

3. **Set Environment Variables**:
   - Vercel will show a form to set environment variables
   - Add all variables from your `.env` file:
     ```
     DB_CONNECTION = postgres
     DATABASE_URL = postgresql://postgres:...
     SECRET_KEY = (generate a new strong key)
     SUPABASE_URL = https://xxxxx.supabase.co
     SUPABASE_KEY = your-anon-key
     SUPABASE_SERVICE_KEY = your-service-role-key
     SUPABASE_BUCKET_NAME = lecture-notes
     ```

4. **Deploy**:
   - Click **"Deploy"**
   - Vercel will build and deploy your application
   - Your app will be available at `https://your-project.vercel.app`

5. **Initialize Database on Vercel**:
   - After first deployment, you need to initialize the database
   - Use Vercel's **Deployments** page to view the deployment logs
   - The `init_db.py` script will have run automatically during build if configured in `package.json`
   - If not, you can run it manually via the Vercel CLI:
     ```bash
     vercel env pull
     python init_db.py
     ```

## Security Best Practices

1. **Keep `.env` file out of version control**:
   - `.env` is listed in `.gitignore`
   - Only commit `.env.example`

2. **Use strong passwords**:
   - Your Supabase database password
   - Your Flask `SECRET_KEY` (generate a random string)

3. **Rotate keys regularly**:
   - In production, rotate your Supabase API keys periodically
   - Go to **Settings > API** in Supabase to manage keys

4. **Use service role key carefully**:
   - Never expose `SUPABASE_SERVICE_KEY` in frontend code
   - Only use it in backend (server-side) code

5. **Set bucket policies**:
   - Ensure your `lecture-notes` bucket allows public reads
   - Consider adding row-level security policies for sensitive data

## Troubleshooting

### "Database connection failed"
- Verify `DATABASE_URL` is correct
- Check that your Supabase project is active (not paused)
- Ensure your Supabase IP whitelist allows your server's IP (usually auto-configured)

### "Supabase authentication failed"
- Verify `SUPABASE_URL` and `SUPABASE_KEY` are correct
- Check that you're using the **anon** key for `SUPABASE_KEY`, not the service role key
- For testing, try using the service role key temporarily to debug

### "File upload failing"
- Verify `SUPABASE_BUCKET_NAME` is correct (default: `lecture-notes`)
- Check that the bucket is **public** (not private)
- Ensure your service role key has permission to write to the bucket
- Check file size doesn't exceed Supabase limits

### "Files can't be downloaded"
- Verify the bucket is public
- Check file permissions in Supabase Storage
- Ensure the file path is being stored correctly in the database

## Switching Back to Local/MySQL

If you want to switch back to local development:

1. Edit `.env`:
   ```env
   DB_CONNECTION=sqlite
   ```

2. Restart the application and database will revert to SQLite

For MySQL:
   ```env
   DB_CONNECTION=mysql
   DATABASE_URL=mysql+pymysql://user:password@localhost/lnsp
   ```

## Additional Resources

- **Supabase Documentation**: https://supabase.com/docs
- **PostgreSQL Documentation**: https://www.postgresql.org/docs/
- **Vercel Documentation**: https://vercel.com/docs
- **Flask SQLAlchemy**: https://flask-sqlalchemy.palletsprojects.com/

## Support

For issues or questions:
1. Check Supabase documentation: https://supabase.com/docs
2. Review your Supabase project logs in the dashboard
3. Check Vercel deployment logs for deployment issues
4. Review application logs for runtime errors
