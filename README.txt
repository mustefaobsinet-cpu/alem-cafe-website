ALEM CAFE - DJANGO DEMO WEBSITE
================================
This is a customizable Django cafe ordering website prepared as a demonstration proposal for Alem Cafe, Dire Dawa.

IMPORTANT BUSINESS / VERIFICATION NOTES
----------------------------------------
- The cafe's exact menu and prices were not reliably available in public sources. Do NOT treat the demo menu as confirmed. Add the real menu, photos, spelling, sizes and prices only after the owner approves them.
- The contact numbers entered from the project request are defaults: phone/SMS contact 0913856409 and Telebirr 0913856407. Confirm these with the cafe owner before publishing.
- CBE, Awash Bank and Abyssinia Bank are NOT pre-filled with invented account numbers. Add only accounts supplied and approved by the cafe owner in Owner Settings > Payment methods.
- The checkout collects a payment reference but does NOT connect to a bank, Telebirr, or verify payment automatically. The owner must check their official account and manually tick Payment verified in the order admin before accepting an order.
- Automatic outbound SMS is NOT enabled. A legitimate SMS gateway account, sender ID/permissions, and credentials from the owner/provider are needed. Do not promise automatic SMS until tested. The customer sees an order reference and pending status after submitting.
- This is a local demonstration starter, not production-ready. Before public deployment, configure a strong environment SECRET_KEY, DEBUG=False, ALLOWED_HOSTS, HTTPS, secure cookies, PostgreSQL, backups, static/media hosting, logging, and privacy/terms pages. Do not deploy with the sample development key or DEBUG=True.
- The owner must approve branding, menu, prices, contact/payment accounts, and ownership/hosting terms before sale.

RUN ON WINDOWS 10 (VS CODE)
---------------------------
1. Extract the ZIP.
2. Open the extracted alem_cafe folder in VS Code (the folder containing manage.py).
3. Open Terminal > New Terminal. If using Command Prompt, run:
   py -m venv .venv
   .venv\Scripts\activate.bat
   python -m pip install -r requirements.txt
   python manage.py makemigrations cafe
   python manage.py migrate
   python manage.py createsuperuser
   python manage.py runserver
4. Visit http://127.0.0.1:8000/
5. Admin: http://127.0.0.1:8000/admin/
6. Owner dashboard: http://127.0.0.1:8000/owner/ (sign in with the staff/superuser account)

OWNER SETUP CHECKLIST
---------------------
1. Sign in at /admin/.
2. Open Cafe settings and confirm cafe name, public phone, SMS contact and Telebirr number.
3. Add approved payment methods: Telebirr, CBE, Awash Bank, Abyssinia Bank. Add exact account name/number/instructions from the owner.
4. Add real categories and menu products with approved ETB prices and images. Mark products available.
5. Place a test order. Verify the transaction manually in the official account before marking Payment verified.
6. Use Owner dashboard to review orders; use /owner/account/ to change the staff username and password.

CUSTOMER PAGES
--------------
Home: /
Menu: /menu/
Cart: /cart/
Checkout: /checkout/

OWNER PAGES
-----------
Owner dashboard: /owner/
Owner settings shortcuts: /owner/settings/
Change username/password: /owner/account/
Django admin: /admin/

TECHNOLOGY
----------
Python + Django + SQLite for local development; HTML/CSS templates; responsive black and gold theme; English and Amharic labels.
