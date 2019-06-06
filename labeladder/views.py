import io

from django.db import transaction

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from labeladder.forms import PageForm
from labeladder.facebook import *

# Create your views here.
from labeladder.models import FacebookPage, User, FacebookLabel
from labeladder.user_id_handler import UserIdHandler


@transaction.atomic
def savelabel_userlist(facebook_page, label_id, users):
    for user in users:
        user_db, created = User.objects.get_or_create(user_id=user)
        faccebook_label = FacebookLabel.objects.get_or_create(page=facebook_page, label_id=label_id,
                                                              owner=user_db)


def enter_page(request):
    form = PageForm()
    if request.method == "POST":
        form = PageForm(request.POST, request.FILES)
        if form.is_valid():
            page_id = form.data["page_id"]
            page_authtoken = form.data["page_authtoken"]
            user_data = request.FILES['csv_file'].read().decode("utf-8")
            user_data = user_data.split("\n")
            label_id = form.data["label_id"]
            list_of_labels = Facebook.get_list_of_labels(page_authtoken)
            labels_str = ""
            facebook_page, created = FacebookPage.objects.get_or_create(access_token=page_authtoken, id=page_id)
            for label in list_of_labels:
                labels_str += "<li>" + label[0] + "\t" + label[1] + "</li>"
            if label_id == "":
                return render(request, "page_file.html", {'form': form, "list": list_of_labels})
            else:
                list_of_requests = Facebook.build_label_url_for_all_users(label_id, page_authtoken, user_data)
                savelabel_userlist(facebook_page, label_id=label_id,users=user_data)
                batch_list_requests = Facebook.batch_requests_builder(list_of_requests, page_authtoken)
                for files in batch_list_requests:
                    requests.post(BASE_URL, files=files)
                return HttpResponse("{success:True}")

    return render(request, "page_file.html", {'form': form, 'response': ""})
