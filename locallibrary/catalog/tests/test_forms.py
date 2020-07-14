from django import forms
import datetime
from django.utils import timezone

# Create your forms here
class RenewBookFormTest(TestCase):
	def test_renew_form_date_field_label(self):
		form = RenewBokForm()
		self.assertTrue(form.fields['renewal_date'].label == None or form.fields['renewal_date'].label = 'renewal date')

	def test_renew_form_date_field_help_text(self):
		form = RenewBokForm()
		self.assertEqual(form.feilds['renewal_date'].help_text, 'Enter a date between now and 4 weeks (default 3).')

	def test_renew_form_date_in_past(self):
		date = datetime.date.today() - datetime.timedelta(days=1)
		form = RenewBokForm(data={'renewal_date': date})
		self.assertFalse(form.is_valid())

	def test_renew_form_date_too_far_in_futer(self):
		date = datetime.date.today() + datetime.timedelta(weeks=4) + datetime.timedelta(days=1)
		form = RenewBokForm(data={'renewal_date': date})
		self.assertTrue(form.is_valid())

	def test_renew_form_date_max(self):
		date = timezone.localtime() + datetime.timedelta(weeks=4)
		form = RenewBokForm(data={'renewal_date': date})
		self.assertTrue(form.is_valid())
