from flask import (render_template, url_for, request, redirect)
from models import (db, Booking, Report, Creative, ContentProviderGroup, Dashboard, app, datetime)
from content_providers import ENTERTAINMENT_CPS, KIDS_CPS, CHANNEL_4, CHANNEL_5, UKTV, SKY
import csv
import os

app.config['UPLOAD_FOLDER'] = "/Users/michaeljones/Documents/Personal Projects/OTIS/static/csv"
# app.config['UPLOAD_FOLDER'] = tempfile.TemporaryDirectory().name
ALLOWED_EXTENSIONS = {'csv'}


# --------------------------------Routing--------------------------------


@app.route('/')
def index():
	campaigns = Booking.query.all()
	today = datetime.date.today()
	return render_template('index.html', campaigns=campaigns, today=today)


@app.route('/dashboard')
def dashboard():
	dashboard = ContentProviderGroup.query.all()
	entertainment = ContentProviderGroup.query.filter(content_provider_group='3|Ex Kids Content')
	kids = ContentProviderGroup.query.filter_by(content_provider_group='3|Kids Content')
	populate_dashboard()
	return render_template('dashboard.html', dashboard=dashboard, entertainment=entertainment, kids=kids)


@app.route('/filtered_campaigns',  methods=['GET', 'POST'])
def filtered_campaigns():
	start_date = request.form['from']
	end_date = request.form['to']
	
	filtered_campaigns = Booking.query.filter(Booking.start_date>=start_date, Booking.end_date<=end_date)
	for campaign in filtered_campaigns:
		campaign.delivered_impressions = campaign_total(campaign.element_number)
		campaign.percentage_delivered = percentage_delivered(campaign.element_number)
		campaign.daily_average = daily_average(campaign.element_number)
		campaign.delivery_pacing = campaign_pace(campaign.element_number)
		campaign.status = campaign_status(campaign.element_number)

	return render_template('campaigns.html', campaigns=filtered_campaigns)

@app.route('/campaigns', methods=['GET', 'POST'])
def campaigns():
	campaigns = Booking.query.all()
	for campaign in campaigns:
		campaign.delivered_impressions = campaign_total(campaign.element_number)
		campaign.percentage_delivered = percentage_delivered(campaign.element_number)
		campaign.daily_average = daily_average(campaign.element_number)
		campaign.delivery_pacing = campaign_pace(campaign.element_number)
		campaign.status = campaign_status(campaign.element_number)

		db.session.commit()

	return render_template('campaigns.html', campaigns=campaigns)


@app.route('/ch4')
def channel4():
	return render_template('channel4.html')


@app.route('/detail/<id>')
def campaign_details(id):
	campaign = Booking.query.get(id)
	campaign_details = Report.query.filter(Report.element_number == campaign.element_number)
	clock_details = Creative.query.filter(Creative.element_number == campaign.element_number)
	return render_template('campaign_details.html', campaign=campaign, campaign_details=campaign_details, clock_details=clock_details)


@app.route('/add_campaign', methods=['GET', 'POST'])
def add_campaign():
	if request.form:
		new_campaign = Booking(status=request.form['status'], 
			element_number=request.form['element_id'], 
			campaign_name=request.form['campaign_name'], 
			cpm_rate=request.form['cpm_rate'], 
			break_seperation=request.form['break_seperation'], 
			targeting=request.form['targeting'], 
			start_date=datetime.datetime.strptime(request.form['start_date'], '%d/%m/%Y'), 
			end_date=datetime.datetime.strptime(request.form['end_date'], '%d/%m/%Y'), 
			daily_average=0,
			booked_impressions=request.form['booked_impressions'],
			delivered_impressions=0,
			delivery_pacing = 0)
		db.session.add(new_campaign)
		db.session.commit()
		return redirect(url_for('campaigns'))
	return render_template('add_campaign.html')


@app.route('/add_creative', methods=['GET', 'POST'])
def add_creative():
	if request.form:
		new_clock = Creative(element_number=request.form['element_number'],
			clock_number=request.form['clock_number'],
			start_date=datetime.datetime.strptime(request.form['start_date'], '%d/%m/%Y'), 
			end_date=datetime.datetime.strptime(request.form['end_date'], '%d/%m/%Y'), 
			)
		db.session.add(new_clock)
		db.session.commit()
		return redirect(url_for('campaigns'))
	return render_template('add_creative.html')

@app.route('/delete/<id>')
def delete_campaign(id):
	campaign = Booking.query.get(id)
	db.session.delete(campaign)
	db.session.commit()
	return redirect(url_for('campaigns'))


@app.route('/edit/<id>', methods=['GET', 'POST'])
def edit_campaign(id):
	booking = Booking.query.get_or_404(id)
	if request.form:
		booking.status=request.form['status']
		booking.element_number=request.form['element_id']
		booking.campaign_name=request.form['campaign_name']
		booking.cpm_rate=request.form['cpm_rate']
		booking.booked_impressions=request.form['booked_impressions']
		booking.break_seperation=request.form['break_seperation']
		booking.targeting=request.form['targeting']
		booking.start_date=datetime.datetime.strptime(request.form['start_date'], '%d/%m/%Y')
		booking.end_date=datetime.datetime.strptime(request.form['end_date'], '%d/%m/%Y')
		db.session.commit()
		return redirect(url_for('campaigns'))
	return render_template('edit_campaign.html', booking=booking)


@app.route('/upload_csv', methods=['GET', 'POST'])
def upload_csv():
	if request.method == "POST":
		if request.files:
			csv = request.files["csv"]
			csv.save(os.path.join(app.config["UPLOAD_FOLDER"], csv.filename))
			print("CSV Saved!")
			add_csv()
			delete_csv()
			return redirect(request.url)
	return render_template('campaigns.html')


@app.route('/bulk_upload', methods=('GET', 'POST'))
def bulk_upload():
	if request.method == "POST":
		if request.files:
			csv = request.files["csv"]
			csv.save(os.path.join(app.config["UPLOAD_FOLDER"], csv.filename))
			print("Bulk Upload SAVED!")
			bulk_upload()
			delete_csv()
			return redirect(request.url)
	return render_template('campaigns.html')


@app.route('/third_party_upload', methods=('GET', 'POST'))
def third_party_upload():
	return render_template('campaigns.html')


@app.route('/upload_dashboard_csv', methods=['GET', 'POST'])
def upload_dashboard_csv():
	if request.method == "POST":
		if request.files:
			csv = request.files["csv"]
			csv.save(os.path.join(app.config["UPLOAD_FOLDER"], csv.filename))
			print("CSV Saved!")
			add_dashboard_csv()
			delete_csv()
			return redirect(request.url)
	return render_template('index.html')


@app.route('/creatives')
def creatives():
	return render_template('creatives.html')

# -----------------------------------------------------------------------

# --------------------------------Methods--------------------------------

def allowed_file(filename):
	return '.' in filename and \
		filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


def campaign_status(element_number):
	campaign = Booking.query.filter_by(element_number=element_number)
	today = datetime.date.today()
	for camp in campaign:
		if camp.status == 'Paused':
			return 'Paused'
		elif camp.status == 'Cancelled':
			return 'Cancelled'
		elif int(camp.delivered_impressions) == 0:
			# print(f'{camp.element_number} IS NOT LIVE')
			return 'Pending'
		elif int(camp.delivered_impressions) > 0 and today < camp.end_date:
			# print(f'{camp.element_number} IS LIVE')
			return 'Live'
		elif int(camp.delivered_impressions) >= int(camp.booked_impressions):
			print(f'{camp.element_number} delivered {camp.delivered_impressions} out of {camp.booked_impressions}')
			return 'Completed'
		elif int(camp.delivered_impressions) < int(camp.booked_impressions) and today < camp.end_date:
			# print(f'{camp.element_number} UNDER-DELIVERED')
			return 'Under-delivered'



def campaign_total(element_number):
	campaign = Report.query.filter_by(element_number=element_number)
	total = 0
	for camp in campaign:
		total += camp.delivered_impressions
	
	return total


def percentage_delivered(element_number):
	campaign = Booking.query.filter_by(element_number=element_number)
	for camp in campaign:
		try:
			delivered_percent = int(100 * float(camp.delivered_impressions) / float(camp.booked_impressions))
		except TypeError:
			delivered_percent = 0
	
	return str(delivered_percent) + "%"


def daily_average(element_number):
	#Calculate the average impressions is needed per day to deliver full.
	campaign = Booking.query.filter_by(element_number=element_number)
	today = datetime.date.today()

	for camp in campaign:
		if today >= camp.end_date:
			average = 0
		elif today <= camp.start_date:
			days_running = (camp.end_date - camp.start_date)
			# print(f'{camp.campaign_name} Days Running: {days_running}')
			days_run = (days_running.days)
			average = camp.booked_impressions / (days_run + 1)
			return int(average)
		elif today >= camp.start_date:
			days_running = (camp.end_date - today)
			days_run = (days_running.days)
			# print(f'{camp.campaign_name} Days Running: {days_running}')	
			remaining_impr = int(camp.booked_impressions) - int(camp.delivered_impressions)
			average = remaining_impr / (days_run + 1)
			return int(average)

		return int(average)

def campaign_pace(element_number):
	#Calculate the pace of the campaign. Is it on target to deliver in full.
	#Pacing = (Days Ran % / Impressions Delivered %)
	campaign = Booking.query.filter_by(element_number=element_number)
	today = datetime.date.today()

	for camp in campaign:
		if camp.delivered_impressions != 0:
			days_running = (camp.end_date - camp.start_date)
			impressions_percentage = (camp.delivered_impressions / camp.booked_impressions) * 100

			if today <= camp.end_date:
				days_ran = (today - camp.start_date)
				days_percentage = (days_ran / days_running) * 100
				campaign_pacing = int(impressions_percentage - days_percentage)
				return str(campaign_pacing) + "%"

			elif today > camp.end_date:
				days_ran = (camp.end_date - camp.start_date)
				days_percentage = (days_ran / days_running) * 100
				campaign_pacing = int(impressions_percentage - days_percentage)
				return str(campaign_pacing) + "%"
		else:
			return str(0) + "%"


def bulk_upload():
	with open('/Users/michaeljones/Documents/Personal Projects/OTIS/static/csv/bookings.csv') as csvfile:
		data = csv.DictReader(csvfile)
		for row in data:
			status = ""
			element_number = row['\ufeffelement number']
			campaign_name = row['campaign name']
			cpm_rate = row['cpm rate']
			start_date = datetime.datetime.strptime(row['start date'], '%d/%m/%Y').date()
			end_date = datetime.datetime.strptime(row['end date'], '%d/%m/%Y').date()
			break_seperation = ""
			targeting = ""
			booked_impressions = row['booked impressions'].replace(',', '')

			bulk_upload_data = Booking(status=status, element_number=element_number, campaign_name=campaign_name, cpm_rate=cpm_rate, start_date=start_date, end_date=end_date, booked_impressions=booked_impressions, break_seperation=break_seperation, targeting=targeting)

			db.session.add(bulk_upload_data)
			db.session.commit()


def add_csv():
	with open("/Users/michaeljones/Documents/Personal Projects/OTIS/static/csv/OTIS Campaign Delivery - Yesterday.csv") as csvfile:
		data = csv.DictReader(csvfile)
		for row in data:
			element_number = row['Campaign External ID']
			date = datetime.datetime.strptime(row['Date'], '%d/%m/%Y').date()
			delivered_impressions = row['Impressions'].replace(',', '')

			new_data = Report(element_number=element_number, date=date, delivered_impressions=delivered_impressions)
			booked_in_db = db.session.query(Report).filter(Report.element_number==new_data.element_number, Report.date==new_data.date).one_or_none()

			if booked_in_db != None:
				#The Report details does exist in the DB.
				print(f'{booked_in_db.element_number} EXISTS')
				if int(booked_in_db.delivered_impressions) != int(new_data.delivered_impressions):
					#The delivered numbers do not match. There is most likely an updated 'delivered_impressions' amount on that day and 'element_number'.
					booked_in_db.delivered_impressions = new_data.delivered_impressions
					db.session.commit()
			elif booked_in_db == None:
				#The Report details does not exist in the DB.
				db.session.add(new_data)
				db.session.commit()


def add_dashboard_csv():
	with open('/Users/michaeljones/Documents/Personal Projects/OTIS/static/csv/OTIS CP Group Inventory - Yesterday.csv') as csvfile:
		data = csv.DictReader(csvfile)
		for row in data:
			date = datetime.datetime.strptime(row['Date'], '%d/%m/%Y').date()
			content_provider_group = row['Content Group']
			inventory = row['Inventory'].replace(',', '')
			delivered_impressions = row['Impressions'].replace(',', '')
			str = row['STR %']
			vtr = row['VTR %']

			dashboard_data = ContentProviderGroup(date=date, content_provider_group=content_provider_group, inventory=inventory, delivered_impressions=delivered_impressions, str=str, vtr=vtr)
			dashboard_in_db = db.session.query(ContentProviderGroup).filter(ContentProviderGroup.content_provider_group==dashboard_data.content_provider_group, ContentProviderGroup.date==dashboard_data.date).one_or_none()

			if dashboard_in_db != None:
				# if dashboard_data.inventory != dashboard_in_db.inventory:
				# 	if dashboard_data.delivered_impressions != dashboard_in_db.delivered_impressions:
				# 		dashboard_in_db.inventory = dashboard_data.inventory
				# 		dashboard_in_db.delivered_impressions = dashboard_data
				# 		db.session.commit()
				pass
			elif dashboard_in_db == None:
				db.session.add(dashboard_data)
				db.session.commit()



def populate_dashboard():
	#Populate the Dashboard table and combine data within the two groups (Entertainment & Kids).
	content_provider = ContentProviderGroup.query.all()
	

def delete_csv():
	if os.path.exists("/Users/michaeljones/Documents/Personal Projects/OTIS/static/csv/OTIS Campaign Delivery - Yesterday.csv"):
		print("FILE EXISTS")
		os.remove("/Users/michaeljones/Documents/Personal Projects/OTIS/static/csv/OTIS Campaign Delivery - Yesterday.csv")
		print("FILE DELETED")
	elif os.path.exists("/Users/michaeljones/Documents/Personal Projects/OTIS/static/csv/OTIS CP Group Inventory - Yesterday.csv"):
		os.remove("/Users/michaeljones/Documents/Personal Projects/OTIS/static/csv/OTIS CP Group Inventory - Yesterday.csv")
	elif os.path.exists("/Users/michaeljones/Documents/Personal Projects/OTIS/static/csv/bookings.csv"):
		os.remove("/Users/michaeljones/Documents/Personal Projects/OTIS/static/csv/bookings.csv")

# -----------------------------------------------------------------------

if __name__ == '__main__':
	db.create_all()
	app.run(debug=True, port=8000, host='127.0.0.1')