import json
from flask import jsonify, request, g, abort
from api import api
from db.shared import db
from db.models.user_post import UserPost
from db.models.post import Post
from db.models.user import User
from sqlalchemy.sql import text
from db.utils import row_to_dict
from middlewares import auth_required


@api.post("/posts")
@auth_required
def add_post():
    # validation
    user = g.get("user")
    if user is None:
        return abort(401)

    data = request.get_json(force=True)
    text = data.get("text", None)
    tags = data.get("tags", None)
    if text is None:
        return jsonify({"error": "Must provide text for the new post"}), 400

    # Create new post
    post_values = {"text": text}
    if tags:
        post_values["tags"] = tags

    post = Post(**post_values)
    db.session.add(post)
    db.session.commit()

    user_post = UserPost(user_id=user.id, post_id=post.id)
    db.session.add(user_post)
    db.session.commit()

    return row_to_dict(post), 200

@api.get("/posts")
@auth_required
def get_posts_by_authorIds():
    data = request.get_json(force=True)
    authorIds = data.get("authorIds",None)
    sortBy = data.get("sortBy",None)
    direction = data.get("direction",None)
    authorList = []
    authorSet = set()
    validationErrors = []

    #Validate authorIds
    if authorIds is None:
        validationErrors.append({"error":"authorIds is a required parameter"})

    else:
        authorList = authorIds.split(",")
        for authorId in authorList:
            if authorId.isdigit():
                authorSet.add(authorId)
            else:
                validationErrors.append({"error":"authorIds must be a list of integers seperated by a comma"})
                    
    #Validate sortBy
    if sortBy is None:
        sortBy = "id"
    else:
        if not sortBy in {"id","reads","likes","popularity"}:
             validationErrors.append({"error":"sortBy must be either id, reads, likes or popularity"})
        
    #Validate direction
    if direction is None:
        direction = "asc"
    else:
        if not direction in {"asc","desc"}:
             validationErrors.append({"error":"direction must be either asc (ascending) or desc (descending)"})

    #If there are any validation errors, display them to the user
    if len(validationErrors) > 0:
        return json.dumps(validationErrors), 400
    
    #Build search logic
    orderText = sortBy + " " + direction
    user_posts = UserPost.query.filter(UserPost.user_id.in_(authorList)).all()
    postIds = set()
    resultsSet = {"posts": []}

    for userPostResult in user_posts:
        postIds.add(userPostResult.post_id)

    postResults = Post.query.filter(Post.id.in_(postIds)).order_by(text(orderText)).all()

    #Format the results
    for postResult in postResults:
        record = {
            "id": postResult.id,
            "likes": postResult.likes,
            "populatiy": postResult.popularity,
            "tags": postResult.tags,
            "text": postResult.text
        }
        resultsSet["posts"].append(record)
    
    return json.dumps(resultsSet,indent=4, sort_keys=True), 200

@api.patch('/posts/<id>')
@auth_required
def patch_post(id):
    data = request.get_json(force=True)
    authorIds = data.get("authorIds",None)
    tags = data.get("tags",None)
    text = data.get("text",None)
    authorSet = set()
    tagList = []
    validationErrors = []
    postRecord = Post.query.get(id)
    authorsRecord = UserPost.query.filter(UserPost.post_id == id).all()
    isUpdate = False
    resultsSet = {"posts": []}

    if authorIds is None:
        for userRecord in authorsRecord:
            authorSet.add(userRecord.user_id)
    else:
        for authorId in authorIds:
            user = None
            user = User.query.filter(User.id == authorId).one()
            if user is None:
                validationErrors.append({"error":"authorId " + str(id) + " is not a valid user id"})
            else:
                authorSet.add(authorId)
                isUpdate = True
    
    if text is None:
        text = postRecord.text

    if tags is None:
        tagList = postRecord.tags
    else:
        tagList = tags

    #If there are any validation errors, display them to the user
    if len(validationErrors) > 0:
        return json.dumps(validationErrors), 400
    
    #if authors are updated, update the UserPost record
    if isUpdate:
        update_authors(authorSet,id)
    
    #update the post record
    postRecord.tags = tagList
    postRecord.text = text
    db.session.commit()

    record = {
        "id": id,
        "authorIds": list(authorSet),
        "likes": postRecord.likes,
        "populatiy": postRecord.popularity,
        "reads": postRecord.reads,
        "tags": tagList,
        "text": text
    }

    resultsSet["posts"].append(record)

    return json.dumps(resultsSet,indent=4, sort_keys=True), 200

def update_authors(authorSet,postId):
    UserPost.query.filter(UserPost.post_id == postId).delete()
    for authorId in authorSet:
        user_post = UserPost(user_id=authorId, post_id=postId)
        db.session.add(user_post)
        db.session.commit()
