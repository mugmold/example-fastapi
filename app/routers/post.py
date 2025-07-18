from fastapi import APIRouter, HTTPException, Request, Response, status, Depends
from fastapi.responses import HTMLResponse, JSONResponse
from app.schemas.post import PostCreate, PostUpdate, PostResponse
from app.core.db_raw import get_connection
from app.core.db import get_db
from app.models.post import Post as post_model
from typing import List, Optional
from sqlalchemy.orm import Session, joinedload
from app.auth.oauth2 import get_current_user
from app.models.user import User as user_model
from app.models.vote import Vote as vote_model
from sqlalchemy import or_, and_, func

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)


def format_post_response(result_tuple):
    post, vote_count = result_tuple
    response_data = post.__dict__
    response_data['total_votes'] = vote_count
    response_data['owner'] = post.owner
    return response_data


@router.get("/", response_model=List[PostResponse])
def get_all_posts(db: Session = Depends(get_db), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    base_query = db.query(
        post_model, func.count(vote_model.post_id).label("total_votes")
    ).join(
        vote_model, vote_model.post_id == post_model.id, isouter=True
    ).group_by(
        post_model.id
    )

    posts = base_query.filter(
        or_(
            post_model.title.icontains(search),
            post_model.content.icontains(search)
        )
    ).limit(limit=limit).offset(offset=skip).all()

    return [format_post_response(post) for post in posts]


@router.get("/me", response_model=List[PostResponse])
def get_my_posts(db: Session = Depends(get_db), current_user: user_model = Depends(get_current_user),
                 limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    base_query = db.query(
        post_model, func.count(vote_model.post_id).label("total_votes")
    ).join(
        vote_model, vote_model.post_id == post_model.id, isouter=True
    ).group_by(
        post_model.id
    )

    posts = base_query.filter(
        and_(
            post_model.user_id == current_user.id,
            or_(
                post_model.title.icontains(search),
                post_model.content.icontains(search)
            )
        )
    ).limit(limit=limit).offset(offset=skip).all()

    return [format_post_response(post) for post in posts]


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=PostResponse)
def create_post(post: PostCreate, db: Session = Depends(get_db), current_user: user_model = Depends(get_current_user)):
    new_post = post_model(user_id=current_user.id, **post.model_dump())
    db.add(new_post)
    db.commit()

    return get_post(id=new_post.id, db=db)


@router.delete("/{id}", status_code=status.HTTP_200_OK, response_model=PostResponse)
def delete_post(id: int, db: Session = Depends(get_db), current_user: user_model = Depends(get_current_user)):
    query = db.query(post_model).filter(post_model.id == id)
    post = query.first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} does not exist")

    if post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")

    query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", status_code=status.HTTP_200_OK, response_model=PostResponse)
def update_post(id: int, post_update: PostUpdate, db: Session = Depends(get_db), current_user: user_model = Depends(get_current_user)):
    query = db.query(post_model).filter(post_model.id == id)
    post = query.first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} does not exist")

    if post.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not allowed!")

    update_data = post_update.model_dump(exclude_unset=True)

    query.update(update_data, synchronize_session=False)
    db.commit()

    return get_post(id=id, db=db)


def get_post(id: int, db: Session = Depends(get_db)):
    base_query = db.query(
        post_model, func.count(vote_model.post_id).label("total_votes")
    ).join(
        vote_model, vote_model.post_id == post_model.id, isouter=True
    ).group_by(
        post_model.id
    )

    result = base_query.filter(post_model.id == id).first()

    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} was not found")

    return format_post_response(result)


@router.get("/{id}", response_class=HTMLResponse)
def get_post_html(id: int, db: Session = Depends(get_db)):
    result = db.query(
        post_model, func.count(vote_model.post_id).label("total_votes")
    ).join(
        vote_model, vote_model.post_id == post_model.id, isouter=True
    ).group_by(
        post_model.id
    ).filter(post_model.id == id).first()

    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} does not exist")

    post, total_votes = result

    return f"""
        <html>
            <head>
                <title>{post.title}</title>
            </head>
            <body>
                <h1>{post.title}</h1>
                <h3>author : {post.owner.username}</h3>
                <h4>total upvotes : {total_votes}</h4>
                <p style='white-space: pre-wrap'>{post.content}</p>
            </body>
        </html>
    """
