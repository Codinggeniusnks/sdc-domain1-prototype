# Replit Production Deployment Manual Publish Steps

**Project:** National AI Workforce Reskilling & Foresight Engine v1.0.0 (`AI Skills Compass`)  
**Deployment Status:** `AUTHENTICATION_REQUIRED` (Repository is 100% deploy-ready; pending user 1-click Replit authentication)  
**Target Environment:** Replit Autoscale Deployment (Dynamic Python 3.11 Runtime)  
**Repository Source:** `https://github.com/Codinggeniusnks/sdc-domain1-prototype.git`

---

## 🚀 1-Click Publishing Instructions

Because the application is built on the Python 3 Standard Library with `.replit` already fully configured, publishing to a live public HTTPS URL on Replit takes **under 60 seconds**:

### Step 1: Open or Import Project in Replit
1. Navigate to [replit.com](https://replit.com).
2. Click **"+ Create Repl"** → Select **"Import from GitHub"**.
3. Paste repository URL: `https://github.com/Codinggeniusnks/sdc-domain1-prototype.git`.
4. Language will automatically detect as **Python**.

### Step 2: Verify Pre-Configured Settings
The `.replit` manifest is already committed in the root directory with the exact required configuration:
- **Run Command:** `python src/main.py`
- **Language / Environment:** `python-3.11`
- **Internal Port:** `5000`
- **External Port:** `80`
- **Host Binding:** `0.0.0.0`
- **Required Secrets:** `None` (Zero external API keys needed; system runs 100% self-contained).

### Step 3: Click "Deploy" (Autoscale Deployment)
1. In the top-right corner of the Replit workspace, click **"Deploy"**.
2. Select **"Autoscale"** (Recommended for dynamic web servers, handles 0-to-many scaling).
3. Confirm settings:
   - **Build Command:** *(Leave blank or `pip install -r requirements.txt`)*
   - **Run Command:** `python src/main.py`
4. Click **"Deploy your Repl"**.

### Step 4: Obtain Your Live Production URL
1. Once deployed, Replit will assign a live public URL in the format:
   `https://<your-repl-name>.replit.app`
2. Test the URL in your browser:
   - `https://<your-repl-name>.replit.app/`
   - `https://<your-repl-name>.replit.app/api/health`
3. Paste this live URL into the designated single field in `artifacts/FINAL_USER_INPUT_REQUIRED.md` and `docs/final_submission_answers.md`.
