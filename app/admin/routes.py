from flask import request, current_app, render_template, flash, redirect, url_for
from app import db
from app.admin import bp
from app.models import Post, Comment, Category
from app.main.forms import CategoryForm
from app.utils import redirect_back
from app.decorators import permission_required, admin_required
from flask_login import login_required, current_user

@bp.route('/post/manage')
@login_required
@permission_required('MODERATE')
def manage_post():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.timestamp.desc()).paginate(
        page, per_page=current_app.config['ADMIN_MANAGE_POST_PER_PAGE'])
    return render_template('admin/manage_post.html', page=page, pagination=posts, posts=posts.items)


@bp.route('/comment/manage')
@login_required
@permission_required('MODERATE')
def manage_comment():
    filter_rule = request.args.get('filter', 'all')  # 'all', 'unreviewed', 'admin'
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['ADMIN_MANAGE_COMMENT_PER_PAGE']
    if filter_rule == 'author':
        filtered_comments = Comment.query.filter_by(from_post_author=True)
    elif filter_rule == 'replied':
        filtered_comments = Comment.query.filter(Comment.replied_id!=None)
    else:
        filtered_comments = Comment.query

    comments = filtered_comments.order_by(Comment.timestamp.desc()).paginate(page, per_page=per_page)
    return render_template('admin/manage_comment.html', comments=comments.items, pagination=comments)


@bp.route('/comment/<int:comment_id>/set-comment-status', methods=['POST'])
@login_required
@permission_required('MODERATE')
def set_comment_status(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    if comment.is_hidden:
        comment.is_hidden = False
        flash('Comment displayed.', 'success')
    else:
        comment.is_hidden = True
        flash('Comment hidden.', 'success')
    db.session.commit()
    return redirect_back()


@bp.route('/comment/<int:comment_id>/delete', methods=['POST'])
@login_required
@permission_required('MODERATE')
def delete_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    db.session.delete(comment)
    db.session.commit()
    flash('Comment deleted.', 'success')
    return redirect_back()


@bp.route('/category/manage')
@login_required
@permission_required('MODERATE')
def manage_category():
    return render_template('admin/manage_category.html')


@bp.route('/category/<int:category_id>/edit', methods=['GET', 'POST'])
@login_required
@permission_required('MODERATE')
def edit_category(category_id):
    form = CategoryForm()
    category = Category.query.get_or_404(category_id)
    if category.id == 1:
        flash('You can not edit the default category.', 'warning')
        return redirect(url_for('blog.index'))
    if form.validate_on_submit():
        category.name = form.name.data
        db.session.commit()
        flash('Category updated.', 'success')
        return redirect(url_for('admin.manage_category'))

    form.name.data = category.name
    return render_template('admin/edit_category.html', form=form)


@bp.route('/category/<int:category_id>/delete', methods=['POST'])
@login_required
@permission_required('MODERATE')
def delete_category(category_id):
    category = Category.query.get_or_404(category_id)
    if category.id == 1:
        flash('You can not delete the default category.', 'warning')
        return redirect(url_for('main.index'))
    category.delete()
    flash('Category deleted.', 'success')
    return redirect(url_for('admin.manage_category'))
