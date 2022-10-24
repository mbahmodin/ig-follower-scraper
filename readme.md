## how to use
This tool only scrapes IG followers which IG allows others to see
```bash
python3 -m venv venv
# activate your venv, in my case im using windows powershell
.\venv\Scripts\Activate.ps1

python3 -m pip install -r requirement.txt
# download chromedriver and place it in this root directory
cp .env.example .env
# edit the .env, insert your login cridentials and the user you want to scrape
python3 scrape.py
```