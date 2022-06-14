import os
from flask import Flask, jsonify, request, abort
from models import *
from flask_cors import CORS
from auth import AuthError, requires_auth



def create_app(test_config=None):

    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    '''
    Only to initialise the database with dummy data
    
    '''
    db_drop_and_create_all()
    
    #test to delete rr
    @app.route('/')
    def get_greeting():
        greeting = "!!!!! Welcome to the best Gym app in the world."
        return greeting

    '''
    TEACHERS
    '''

    #Get all teachers from the database
    @app.route('/teachers')
    def get_all_teachers():
        teachers = Teacher.query.all()
        teachers_formatted = [teacher.format() for teacher in teachers]

        return jsonify({
            'success': True,
            'teachers': teachers_formatted
        })
    
    #Add a new teacher (only Gym Manager has permission)
    @app.route('/teachers', methods=['POST'])
    @requires_auth('add:teacher')
    def add_teacher(jwt):
        body = request.get_json()
        new_name = body.get('name', None)
        new_discipline = body.get('discipline_id', None)
        new_instagram_account = body.get('instagram_account', None)

        if new_discipline is None:
            abort(422)
        else:
            try:
                new_teacher = Teacher(name=new_name, discipline_id=new_discipline, instagram_account=new_instagram_account)
                new_teacher.insert()

                teachers = Teacher.query.all()
                teachers_formatted = [teacher.format() for teacher in teachers]

                return jsonify({
                    'success': True,
                    'teachers': teachers_formatted
                })
            except:
                abort(422)

    #Modify an existing teacher (only Gym Manager has permission)
    @app.route('/teachers/<teacher_id>', methods=['PATCH'])
    @requires_auth('patch:teacher')
    def patch_teacher(jwt, teacher_id):
        selected_teacher = Teacher.query.filter(Teacher.id==teacher_id).one_or_none()

        if selected_teacher is None:
            abort(404)
        else:
            try:
                body = request.get_json()
                new_name = body.get('name', selected_teacher.name)
                new_discipline = body.get('discipline_id', selected_teacher.discipline_id)
                new_instagram_account = body.get('instagram_account', selected_teacher.instagram_account)
                selected_teacher.name = new_name
                selected_teacher.discipline_id = new_discipline
                selected_teacher.instagram_account = new_instagram_account
                selected_teacher.update()

                teachers = Teacher.query.all()
                teachers_formatted = [teacher.format() for teacher in teachers]

                return jsonify({
                    'success': True,
                    'teachers': teachers_formatted
                })

            except:
                abort(422)
    
    #Delete an existing teacher (only Gym Manager has permission)
    @app.route('/teachers/<teacher_id>', methods=['DELETE'])
    @requires_auth('delete:teacher')
    def delete_teacher(jwt, teacher_id):
        selected_teacher = Teacher.query.filter(Teacher.id==teacher_id).one_or_none()
        
        if selected_teacher is None:
            abort(404)
        else:
            selected_teacher.delete()

            teachers = Teacher.query.all()
            teachers_formatted = [teacher.format() for teacher in teachers]

            return jsonify({
                'success': True,
                'teachers': teachers_formatted
            })


    '''
    DISCIPLINES
    '''

    #Get all disciplines from the database
    @app.route('/disciplines')
    def get_all_disciplines():
        disciplines = Discipline.query.all()
        disciplines_formatted = [discipline.format() for discipline in disciplines]

        return jsonify({
            'success': True,
            'disciplines': disciplines_formatted
        })
    
    #Add a new discipline (only Gym Manager has permission)
    @app.route('/disciplines', methods=['POST'])
    @requires_auth('add:discipline')
    def add_discipline(jwt):
        body = request.get_json()
        new_name = body.get('name', None)

        if new_name is None:
            abort(422)
        else:
            try:
                new_discipline = Discipline(name=new_name)
                new_discipline.insert()

                disciplines = Discipline.query.all()
                disciplines_formatted = [discipline.format() for discipline in disciplines]

                return jsonify({
                    'success': True,
                    'disciplines': disciplines_formatted
                })
            except:
                abort(422)


    '''
    SESSIONS
    '''

    #Get all sessions from the database
    @app.route('/sessions')
    def get_all_sessions():
        sessions = Session.query.all()
        sessions_formatted = [session.format() for session in sessions]

        return jsonify({
            'success': True,
            'sessions': sessions_formatted
        })
    
    #Add a new session (only Teachers have permission)
    @app.route('/sessions', methods=['POST'])
    @requires_auth('add:sessions')
    def add_session(jwt):
        body = request.get_json()
        new_name = body.get('name', None)
        new_gym = body.get('gym_id', None)
        new_teacher = body.get('teacher_id', None)
        new_discipline = body.get('discipline_id', None)
        new_start_time = body.get('start_time', None)
        new_length_in_minutes = body.get('length_in_minutes', None)


        if None in {new_gym,new_teacher,new_discipline,new_start_time,new_length_in_minutes}:
            abort(422)
        else:
            try:
                new_session = Session(name=new_name,gym_id=new_gym,teacher_id=new_teacher,discipline_id=new_discipline,start_time=new_start_time,length_in_minutes=new_length_in_minutes)
                new_session.insert()

                sessions = Session.query.all()
                sessions_formatted = [session.format() for session in sessions]

                return jsonify({
                    'success': True,
                    'sessions': sessions_formatted
                })
            except:
                abort(422)

    # Error Handling

    @app.errorhandler(404)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404


    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422


    @app.errorhandler(AuthError)
    def handle_auth_error(exception):
        # Receive the raised authorization error and propagates it as response
        response = jsonify({
            'success': False,
            'error': exception.status_code,
            'message': exception.error
        }), exception.status_code

        return response


    return app

app = create_app()

if __name__ == '__main__':
    app.run()
