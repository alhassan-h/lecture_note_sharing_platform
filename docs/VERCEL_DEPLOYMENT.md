# Vercel Deployment Guide

This guide explains how to deploy the Lecture Note Sharing Platform to Vercel with Supabase as the backend.

## Quick Summary

1. The application uses **Supabase** for the PostgreSQL database and file storage
2. The application is configured for **Vercel's serverless Python runtime**
3. All configuration uses environment variables (no hardcoded secrets)

## Prerequisites

- A GitHub account with your LNSP repository pushed
- A Supabase account (free at [supabase.com](https://supabase.com))
- A Vercel account (free at [vercel.com](https://vercel.com))
- Your Supabase credentials (see [SUPABASE_SETUP.md](SUPABASE_SETUP.md))

## Deployment Steps

### 1. Set up Supabase (One-time)

Follow the instructions in [SUPABASE_SETUP.md](SUPABASE_SETUP.md) to:
- Create a Supabase project
- Get your database credentials
- Create a storage bucket
- Get your API keys

### 2. Prepare for Deployment

Ensure your code is pushed to GitHub:

```bash
git add .
git commit -m "Add Supabase integration for Vercel deployment"
git push origin main
```

### 3. Connect to Vercel

1. Go to [vercel.com](https://vercel.com) and log in
2. Click **"Add New Project"**
3. Select your LNSP repository from GitHub
4. Vercel will auto-detect it's a Python project
5. Click **"Import"**

### 4. Set Environment Variables

On the Vercel import screen, you'll see **"Environment Variables"**. Add the following (replace with your actual values from Supabase):

```
DB_CONNECTION=postgres
DATABASE_URL=postgresql://postgres:<password>@db.<project-id>.supabase.co:5432/postgres
SECRET_KEY=<generate-a-random-string>
SUPABASE_URL=https://<project-id>.supabase.co
SUPABASE_KEY=<your-anon-key>
SUPABASE_SERVICE_KEY=<your-service-role-key>
SUPABASE_BUCKET_NAME=lecture-notes
```

**To generate a SECRET_KEY**, you can use Python:
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

Or use an online UUID generator.

### 5. Deploy

1. Click **"Deploy"**
2. Vercel will build and deploy your application
3. Your app will be live at `https://your-project.vercel.app`

### 6. Initialize the Database

After the first deployment:

1. Go to your Vercel project dashboard
2. Click **"Deployments"**
3. Find the first deployment and check the **Build Logs**
4. The `init_db.py` script should have run automatically during the build

If you need to manually initialize:

```bash
vercel env pull    # Download env vars from Vercel
python init_db.py  # Run initialization locally
```

## Understanding the Deployment

### File Structure

- `run.py` - Entry point (WSGI application for Vercel)
- `config.py` - Configuration with environment variable support
- `app/` - Flask application package
- `vercel.json` - Vercel-specific configuration
- `.env.example` - Template for environment variables
- `SUPABASE_SETUP.md` - Detailed Supabase setup guide

### How It Works

1. **Vercel receives your push** to GitHub
2. **Vercel builds** your project:
   - Installs Python 3.x
   - Runs `pip install -r requirements.txt`
   - Detects `run.py` as the entry point
3. **Database initialization** happens automatically if configured
4. **Application starts** and handles HTTP requests
5. **File uploads go to Supabase Storage** (not ephemeral filesystem)
6. **Database queries use Supabase PostgreSQL**

### Why This Works on Vercel

Traditional hosting has a persistent filesystem. Vercel's serverless functions have an **ephemeral filesystem** that resets on each request. This would break:
- Local file uploads (temporary)
- SQLite database (disappears after request)

**Our solution:**
- Uses **managed PostgreSQL** (Supabase) instead of SQLite
- Uses **cloud storage** (Supabase Storage) instead of local filesystem
- Stores only metadata in the database
- No filesystem persistence needed

## Troubleshooting

### Deployment Fails

1. **Check build logs**: Click the deployment in Vercel and view **Build Logs**
2. **Check environment variables**: Ensure all required vars are set in Vercel settings
3. **Check database URL**: Verify your `DATABASE_URL` is correct
4. **Check Python version**: Verify requirements.txt is compatible

### Application Shows 500 Error

1. **Check function logs**: In Vercel dashboard, go to **Logs**
2. **Check Supabase status**: Verify your Supabase project is not paused
3. **Check API keys**: Verify `SUPABASE_KEY` is correct
4. **Database not initialized**: Run the initialization manually

### Files Can't Upload

1. **Check bucket exists**: In Supabase, go to **Storage** and verify `lecture-notes` bucket
2. **Check bucket is public**: Bucket should have public read/write access
3. **Check `SUPABASE_KEY`**: Must be the **anon** key, not service role key
4. **Check file size**: Free tier has limits on file size and storage

### Files Can't Download

1. **Check bucket is public**: Storage bucket must be public
2. **Check file path**: Ensure the file path was stored correctly in database
3. **Check API key**: Verify you're using the right Supabase key

## Monitoring and Maintenance

### View Logs

1. Go to your Vercel project
2. Click **"Logs"** tab
3. Filter by **Build**, **Deployment**, or **Function** logs

### Monitor Database

1. Go to your Supabase project
2. Click **"Database"** to check connection status
3. View **Storage** to see uploaded files
4. Check **Authentication** (logs) for access issues

### Update Environment Variables

1. In Vercel: **Project Settings > Environment Variables**
2. Click the variable to edit or delete it
3. New deployments will use updated variables

### Redeploy

To redeploy without code changes:

1. Go to your Vercel project
2. Click **"Deployments"**
3. Find the deployment you want to redeploy
4. Click **"..."** and **"Redeploy"**

## Scaling Considerations

As your platform grows:

1. **Database performance**: Monitor Supabase logs
2. **Storage limits**: Supabase free tier has 1GB limit
3. **User limits**: Free tier supports 500K monthly active users
4. **Upgrade options**: Supabase offers paid plans when needed

## Security Best Practices

1. **Rotate secrets regularly**:
   - Generate new `SECRET_KEY` monthly
   - Rotate API keys in Supabase **Settings > API**

2. **Keep secrets in Vercel only**:
   - Never commit `.env` file
   - Use Vercel's environment variables, not `.env`

3. **Use HTTPS**:
   - Vercel provides free SSL certificates
   - All traffic is automatically HTTPS

4. **Monitor access**:
   - Check Vercel logs for errors and unusual activity
   - Monitor Supabase activity logs

## Next Steps

1. **Custom domain**: In Vercel **Project Settings > Domains**
2. **CI/CD**: Vercel auto-deploys on every GitHub push
3. **Custom email**: Set up transactional email for user notifications
4. **Analytics**: Add analytics to track user engagement

## Support Resources

- **Vercel Docs**: https://vercel.com/docs
- **Supabase Docs**: https://supabase.com/docs
- **Flask Docs**: https://flask.palletsprojects.com
- **PostgreSQL Docs**: https://www.postgresql.org/docs/

## Reverting to Local Development

To switch back to local SQLite development:

1. Update `.env`:
   ```
   DB_CONNECTION=sqlite
   ```

2. Delete `.env` variables for Supabase if testing locally
3. Restart application

## Performance Tips

1. **Database indexing**: Supabase automatically indexes common queries
2. **Query optimization**: Check database logs for slow queries
3. **Cache headers**: Static files are automatically cached by Vercel
4. **CDN**: Vercel includes a global CDN for fast content delivery
