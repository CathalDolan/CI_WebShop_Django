1. Go to stripe.com
2. Click "Start Now" on the homepage
3. Sign up
    Email: ci_webshop@gizagig.com
    Name: Cathal Dolan
    Password: WebShop_01
4. Go to https://stripe.com/docs/payments/accept-a-payment#web-collect-card-details
    - Copy the "checkout html" script tag
    - Go to base.html and add to the {% block corejs %}
5. pip3 install stripe

Public Key: export STRIPE_PUBLIC_KEY=pk_test_51IPWLOJokGMhDJHUNalrumeiRSXpxX7lqrn1rIVcBR3WlZaANWGqyVU9kZT9MOnA0qrUooomthBSnIgDFKBqMLez00Hcacb58N
Secret Key: export STRIPE_SECRET_KEY=sk_test_51IPWLOJokGMhDJHUDkCWGTSd7V2JcsCglM7z0x0GXdzIwzc1ClitYtGZY1IhAdr3otz2vcy0ia7Wa2b3YkN1Ed8q00Q5kJTr4Z
WebHook Key: export STRIPE_WH_SECRET=whsec_NDeKAXE3JijgrSfTkxb4DE095czBjO2E

echo $STRIPE_WH_SECRET - To see the key

Unable to get WH Keys from Giotpod. GP issue
1. env.py in root
2. import os
3. os.environ["STRIPE_PUBLIC_KEY"] = "pk_test_51IPWLOJokGMhDJHUNalrumeiRSXpxX7lqrn1rIVcBR3WlZaANWGqyVU9kZT9MOnA0qrUooomthBSnIgDFKBqMLez00Hcacb58N"
4. In settings.py
    if os.path.exists("env.py"):
    import env
