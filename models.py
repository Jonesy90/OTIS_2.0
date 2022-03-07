from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import datetime

app = Flask(__name__, template_folder='templates')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///booking.db'
# app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


class Booking(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	status = db.Column('Status', db.String())
	element_number = db.Column('Element #', db.String())
	campaign_name = db.Column('Campaign Name', db.String())
	cpm_rate = db.Column('CPM Rate', db.String())
	break_seperation = db.Column('Break Seperation', db.String())
	targeting = db.Column('Targeting', db.String())
	start_date = db.Column('Start Date', db.Date())
	end_date = db.Column('End Date', db.Date())
	daily_average = db.Column('Daily Average', db.Integer())
	booked_impressions = db.Column('Booked Impressions', db.Integer())
	delivered_impressions = db.Column('Delivered Impressions', db.String())
	percentage_delivered = db.Column('% Delivered', db.String())
	delivery_pacing = db.Column('Delivery Pacing', db.Integer())

	def __repr__(self):
		return f'''Status:{self.status} 
		Element Number: {self.element_number} 
		Campaign Name: {self.campaign_name} 
		CPM Rate: {self.cpm_rate}
		Break Seperation: {self.break_seperation}
		Targeting: {self.targeting}
		Start Date: {self.start_date}
		End Date: {self.end_date}
		Daily Average: {self.daily_average}
		Booked Impressions: {self.booked_impressions}
		Delivered Impressions: {self.delivered_impressions}
		% Delivered: {self.percentage_delivered}
		Delivery Pacing: {self.delivery_pacing}'''


class Report(db.Model):
	__tablename__ = 'report'
	id = db.Column(db.Integer, primary_key=True)
	element_number = db.Column('Element Number', db.String())
	date = db.Column('Date', db.Date())
	delivered_impressions = db.Column('Delivered Impressions', db.Integer())

	def __repr__(self):
		return f'''Element Number: {self.element_number}
		Date: {self.date}
		Delivered Impressions: {self.delivered_impressions}'''


class ContentProviderGroup(db.Model):
	__tablename__ = 'contentprovidergroup'
	id = db.Column(db.Integer, primary_key=True)
	date = db.Column('Date', db.Date())
	content_provider_group = db.Column('Content Provider Group', db.String())
	inventory = db.Column('Inventory', db.Integer())
	delivered_impressions = db.Column('Delivered Impressions', db.Integer())
	str = db.Column('STR %', db.String())
	vtr = db.Column('VTR %', db.String())

	def __repr__(self):
		return f'''Date: {self.date}
		Content Provider Group: {self.content_provider_group}
		Inventory: {self.inventory}
		Delivered Impressions: {self.delivered_impressions}
		STR %: {self.str}
		VTR %: {self.vtr}
		'''


class Dashboard(db.Model):
	__tablename__ = 'dashboard'
	id = db.Column(db.Integer, primary_key=True)
	date = db.Column('Date', db.Date())
	group = db.Column('Content Group', db.String())
	inventory = db.Column('Inventory', db.Integer())
	delivered_impressions = db.Column('Delivere Impression', db.Integer())
	str = db.Column('STR %', db.String())
	vtr = db.Column('VTR %', db.String())

	def __repr__(self):
		return f'''Date: {self.date}
		Content Group: {self.group}
		Inventory: {self.inventory}
		Delivered Impressions: {self.delivered_impressions}
		STR %: {self.str}
		VTR %: {self.vtr}
		'''


class Creative(db.Model):
	__tablename__ = 'creative'
	id = db.Column(db.Integer, primary_key=True)
	element_number = db.Column('Element Number', db.String())
	campaign_name = db.Column('Campaign Name', db.String())
	clock_number = db.Column('Clock Number', db.String())
	start_date = db.Column('Start Date', db.Date())
	end_date = db.Column('End Date', db.Date())
	status = db.Column('Status', db.String())

	def __repr__(self):
		return f'''Element Number: {self.element_number}
		Campaign Name: {self.campaign_name}
		Clock Number: {self.clock_number}
		Start Date: {self.start_date}
		End Date: {self.end_date}
		Status: {self.status}
		'''


class ThirdParty(db.Model):
	__tablename__ = 'thirdparty'
	id = db.Column(db.Integer, primary_key=True)
	date = db.Column('Date', db.Date())
	content_provider = db.Column('Content Provider', db.String())
	ad_request = db.Column('Ad Request', db.Integer())
	ad_decision = db.Column('Ad Decision', db.Integer())
	actual_impressions = db.Column('Actual Impressions', db.Integer())
	ff_adviews = db.Column('FF Ad Views', db.Integer())
	viewed_75 = db.Column('75% Viewed', db.Integer())
	completed_play = db.Column('Complete Play', db.Integer())
	normal_speed_impressions = db.Column('Actual Impressions - FF Impressions', db.Integer())

	def __repr__(self):
		return f'''Date: {self.date}
		Content Provider: {self.content_provider}
		Ad Request: {self.ad_request}
		Ad Decision: {self.ad_decision}
		Actual Impressions: {self.actual_impressions}
		FF Ad Views: {self.ff_adviews}
		75% Viewed: {self.viewed_75}
		Complete Play: {self.completed_play}
		Actual Impressions - FF Impressions: {self.normal_speed_impressions}
		'''