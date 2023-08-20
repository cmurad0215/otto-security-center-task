# otto-security-center-task
Security Center Device matching task for Otto International

This python file assumes 4 files are already present:
1. ARC.csv
   This file is exported from Azure ARC servers list
2. Config.csv
   This file is exported from AWS Config from the Organizational Unit Account (with all accounts selected), with a query (uploaded in some other repo)
3. Security.csv
   This file exported from https://security.microsoft.com then Devices
4. SSM.csv
   This file is exported from AWS Fleet Manager

Finally what the script csvParser.py does is first gets the unique IPs available from the 4 files, and shows us an output of which IP is available in which list.
This helps us take decisions on which IP to remove, install SSM, install ARC and/or check the security center portal.

The script csvParser.py also helps generate instance IDs not available in AWS any more from the list of AWS Config.

This task was initially done by excel and using formulas, and would take approx 2 hours to complete. Now it takes 5 mins approx.


update on 2023-08-20:
The csvParserFunction.py does the same task with Functions implemented.
Also output a new csv file for easier visualization
