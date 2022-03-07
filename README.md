# OTIS 2.0 (Operations Tracker Insight System)

## What it does?
An application hold past, present and future bookings. Calculates the daily delivery required, remaining delivery, delivered percentage and the pacing percentage. This determines which booking requires attention and action, within the given adserving platform.

It holds a number of pages - 
1. Home : Displays any bookings which have a negative 'Delivery Pacing %'. For changes to then be made.
2. Dashboard : Displays the delivery split for both Entertainment and Kids CP (Content Providers) groups.
3. VMUK: Displays delivery data for VMUK. Breaking it down by each campaign which are either Pending, Paused or Live. Cancelled or Completed campaigns will be excluded from this list.
4. CH4 : Displays delivery data for Channel 4.
5. UKTV : Displays delivery data for UKTV.
6. Sky : Displays delivery data for Sky.
7. CH5 : Displays delivery data for Channel 5.

### HOME
<img width="1751" alt="Screenshot 2022-03-07 at 12 43 25" src="https://user-images.githubusercontent.com/4954209/157037110-919d3d4d-9668-4394-927b-fa0b6cdb37c4.png">

### VMUK
<img width="1755" alt="Screenshot 2022-03-07 at 12 45 12" src="https://user-images.githubusercontent.com/4954209/157037170-b36d2a07-ccfe-480a-996b-03bea4a647b5.png">

## Development Setup & Running Application
1. Setup a virtual enviroment with `python3 -m venv env`
2. Activate the virtual enviroment with `source ./env/bin/activate`
3. Install all the libraries within requirements.txt `pip install -r requirements.txt`
4. Run the application `python3 app.py`
