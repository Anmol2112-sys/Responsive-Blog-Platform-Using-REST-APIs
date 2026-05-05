from flask import Flask, request, jsonify
    data = request.json
    post.title = data['title']
    post.content = data['content']
    db.session.commit()
    return jsonify({'msg': 'Updated'})

@app.route('/posts/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_post(id):
    post = Post.query.get(id)
    db.session.delete(post)
    db.session.commit()
    return jsonify({'msg': 'Deleted'})

# ================= COMMENTS CRUD =================
@app.route('/comments', methods=['POST'])
@jwt_required()
def add_comment():
    user_id = get_jwt_identity()
    data = request.json
    comment = Comment(text=data['text'], post_id=data['post_id'], user_id=user_id)
    db.session.add(comment)
    db.session.commit()
    return jsonify({'msg': 'Comment added'})

@app.route('/comments/<int:post_id>', methods=['GET'])
def get_comments(post_id):
    comments = Comment.query.filter_by(post_id=post_id).all()
    return jsonify([{'id': c.id, 'text': c.text} for c in comments])

# ================= RUN =================
if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
