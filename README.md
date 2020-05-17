# CurseForge-Update-List-Getter

Get update list from curse forge update mails which you have subscribed by Google Mail.  

To use google mail api, follow the guideline below.

**[Gmial API QuickStart](https://developers.google.com/gmail/api/quickstart/python)**

Place the __*credentials.json*__ file at root directory  

To use it  

>`python3 main.py`

To extend it to other email servers:

Implement your own IQuerys, and make a main to install it
Reimplement IFilter can filter other mails, also remember install it
