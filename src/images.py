from src.constants.http_status_codes import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_409_CONFLICT
from flask import Blueprint, request
from flask.json import jsonify
from src.database import Image, db

import nasapy
import os
import pandas
from datetime import date, timedelta
import urllib.request


images = Blueprint("images", __name__, url_prefix="/api/v1/images")


@images.post("add_image")
def add_image():
    title = request.get_json().get('title')
    explanation = request.get_json().get('explanation')
    url = request.get_json().get('url')
    hdurl = request.get_json().get('hdurl')

    if Image.query.filter_by(title=title).first():
        return jsonify({
            'error': 'Title already exists'
        }), HTTP_409_CONFLICT
    
    if Image.query.filter_by(url=url).first():
        return jsonify({
            'error': 'URL already exists'
        }), HTTP_409_CONFLICT

    if Image.query.filter_by(hdurl=hdurl).first():
        return jsonify({
            'error': 'HDURL already exists'
        }), HTTP_409_CONFLICT

    image = Image(title=title,explanation=explanation,url=url,hdurl=hdurl)
    db.session.add(image)
    db.session.commit()

    return jsonify({
        'id': image.id,
        'title': image.title,
        'explanation': image.explanation,
        'url': image.url,
        'hdurl': image.hdurl,
    }), HTTP_201_CREATED

@images.get("image_by_title/<fragment>")
def get_image_by_title(fragment):

    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 5, type=int)

    images = Image.query.filter(Image.title.contains(fragment)).paginate(page=page, per_page=per_page)

    if not images:
        return jsonify({'message': 'There are no images that contain ' + str(fragment) + " in their title" }), HTTP_404_NOT_FOUND

    data = []
    for image in images.items:
        data.append(({
        'id': image.id,
        'title': image.title,
        'explanation': image.explanation,
        'url': image.url,
        'hdurl': image.hdurl,
        }))
    
    meta = {
            "page": images.page,
            'pages': images.pages,
            'total_count': images.total,
            'prev_page': images.prev_num,
            'next_page': images.next_num,
            'has_next': images.has_next,
            'has_prev': images.has_prev,

        }

    return jsonify({'data': data, "meta": meta}), HTTP_200_OK

@images.get("image_by_explanation/<fragment>")
def get_image_by_explanation(fragment):

    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 5, type=int)

    images = Image.query.filter(Image.explanation.contains(fragment)).paginate(page=page, per_page=per_page)

    if not images:
        return jsonify({'message': 'There are no images that contain ' + str(fragment) + " in their explanation" }), HTTP_404_NOT_FOUND

    data = []
    for image in images.items:
        data.append(({
        'id': image.id,
        'title': image.title,
        'explanation': image.explanation,
        'url': image.url,
        'hdurl': image.hdurl,
        }))
    
    meta = {
            "page": images.page,
            'pages': images.pages,
            'total_count': images.total,
            'prev_page': images.prev_num,
            'next_page': images.next_num,
            'has_next': images.has_next,
            'has_prev': images.has_prev,

        }

    return jsonify({'data': data, "meta": meta}), HTTP_200_OK

@images.get("image_by_url/<url>")
def get_image_by_url(fragment):

    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 5, type=int)

    image = Image.query.filter(Image.url.contains(fragment)).paginate(page=page, per_page=per_page)

    if not image:
        return jsonify({'message': "There are is no image with that URL" }), HTTP_404_NOT_FOUND

    return jsonify(({
        'id': image.id,
        'title': image.title,
        'explanation': image.explanation,
        'url': image.url,
        'hdurl': image.hdurl,
        }))

    

@images.get("image_by_hdurl/<hdurl>")
def get_image_by_hdurl(fragment):

    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 5, type=int)

    image = Image.query.filter(Image.url.contains(fragment)).paginate(page=page, per_page=per_page)

    if not image:
        return jsonify({'message': "There are is no image with that HDURL" }), HTTP_404_NOT_FOUND

    return jsonify(({
        'id': image.id,
        'title': image.title,
        'explanation': image.explanation,
        'url': image.url,
        'hdurl': image.hdurl,
        }))

@images.get("populate")
def populate():

    key = "3pdvIP08fK1EEb7QJ1HaJliJVaahITfuWeJ36hkF"
    nasa = nasapy.Nasa(key = key)


    start_date = date(2019, 1, 1)
    end_date = date(2020, 5, 1)
    delta = timedelta(days=1)

    while start_date <= end_date:
        apod = nasa.picture_of_the_day(date=start_date.strftime('%Y-%m-%d'), hd=True)
        title = apod["title"]
        explanation = apod["explanation"]
        url = apod["url"]
        if "hdurl" in apod.keys():
            hdurl = apod["hdurl"]
            image = Image(title=title,explanation=explanation,url=url,hdurl=hdurl)
        image = Image(title=title,explanation=explanation,url=url)
        db.session.add(image)
        start_date += delta

    db.session.commit()

    return jsonify(({
        'message': "populated"
        }))