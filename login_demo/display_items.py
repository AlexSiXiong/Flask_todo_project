from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity, jwt_optional

class TodoList(Resource):
    """
    jwt_required - requires a valid JWT to access the endpoint
    """
    @jwt_required(optional=True)
    def get(self):
        user_id = get_jwt_identity()        
        todo_items = None
        if user_id:
            """
            pseudo-code:

            todo_items = [retrive_all_items_in_db where item_created_user_id == user_id]

            """
            return {'items': todo_items}, 200
        return {'message': 'User not logged in.'}, 404