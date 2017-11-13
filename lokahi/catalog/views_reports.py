from catalog.views import serialize, generate_response

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.middleware.csrf import get_token
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q

from catalog.models import Report

@csrf_exempt
def report(request, report_id):
	"""
	GET - return the row in the corresponding database table in JSON.
	POST - be able to update a row in the table given a set of key-value form encoded pairs (PREFERRED, NOT JSON)
	"""
	if request.method == 'GET':
		return __handle_report_get(request, report_id)
	if request.method == 'POST':
		return generate_response("Only GET requests allowed", False)


def __handle_report_get(request, report_id):
	if report_id == 'all':
		result = __filter(Report.objects.all(), request.GET)
		if len(result) == 0: 
			return generate_response("no queries matched filters", True, payload = {"result": []})
		else: 
			return generate_response("found results", True, obj_list = list(result))
	else:
		try:
			report = Report.objects.get(pk=report_id)
			return generate_response("report found", True, book)
		except:
			return generate_response("report not found", False)


def __filter(query_set, filters):
	for key in filters:
		value = filters[key]
		if key == 'id': query_set = query_set.filter(id = value)
	return query_set



@csrf_exempt
def create_report(request):
	"""
	Handles the /report/create endpoint for creating a report and adding it to the database.
	"""
	if request.method == 'POST':
		return __handle_create_report_post(request)
	return generate_response("Only POST requests allowed", False)


def __handle_create_report_post(request):
	try:
		title = request.POST['title']
		year_published = request.POST['year_published']
		rating = request.POST['rating']
		author_id = request.POST['author']
		author = Author.objects.get(pk = author_id)
		report = Report(
			title = title, 
			year_published = year_published,
			rating = rating,
			author = author,
		)
		report.save()
		return generate_response("report saved", True, book)
	except KeyError as e:
		return generate_response("missing %s" % e.args[0].strip("'"), False)
	except Exception as e:
		return generate_response(str(e), False)


@csrf_exempt
def delete_report(request, report_id):
	try:
		report = Report.objects.get(pk=report_id)
		report.delete()
		return generate_response("report deleted", True, report)
	except:
		return generate_response("report does not exist", False)
