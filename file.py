import json
import uuid
from flask import Blueprint, request, jsonify
from sqlalchemy.exc import IntegrityError
from models import session, File
from auth import token_required
import os

file = Blueprint('file' ,__name__, url_prefix='/api')
basedir = os.path.abspath(os.path.dirname(__file__))
imageTypes = ['image/png', 'image/jpeg', 'image/svg', 'image/gif']
videoTypes = ['video/mp4', 'video/mpeg', 'video/ogg']
fileTypes = ['application/vnd.openxmlformats-officedocument.wordprocessingml.document', 'application/gzip', 'application/pdf','application/vnd.openxmlformats-officedocument.presentationml.presentation', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', 'application/zip', 'text/plain']

@file.route('/upload', methods=['POST'])
@token_required
def upload(current_user):
    try:
        if 'file' in request.files:
            file = request.files['file']
            check_file = session.query(File).filter_by(name=file.filename)
            if check_file is None:   
                if file.mimetype in imageTypes:
                    file.save(os.path.join(basedir, 'static', f'{current_user.username}', 'images' , file.filename))
                    new_file = File(name=file.filename, size=len(file.read()), type=file.mimetype, location=f'{current_user.username}/images/{file.filename}', user_id=uuid.UUID(str(current_user.id)))
                    session.add(new_file)
                    session.commit()
                elif file.mimetype in videoTypes:
                    file.save(os.path.join(basedir, 'static', f'{current_user.username}', 'videos' , file.filename))
                    new_file = File(name=file.filename, size=len(file.read()), type=file.mimetype, location=f'{current_user.username}/videos/{file.filename}', user_id=uuid.UUID(str(current_user.id)))
                    session.add(new_file)
                    session.commit()
                elif file.mimetype in fileTypes:
                    file.save(os.path.join(basedir, 'static', f'{current_user.username}', 'docs' , file.filename))
                    new_file = File(name=file.filename, size=len(file.read()), type=file.mimetype, location=f'{current_user.username}/docs/{file.filename}', user_id=uuid.UUID(str(current_user.id)))
                    session.add(new_file)
                    session.commit()
                else:
                    return jsonify({'error':'file type not allowed'}), 400
                return jsonify('new file uploaded'), 201
            else:
                return jsonify({'error':'file with same name exists'}), 400
        else:
            return jsonify({'error':'no file uploaded'}), 400
    except Exception as ex:
        session.rollback()
        return jsonify({'error':'couldnt upload file'}), 400

@file.route('/download/<id>', methods=['GET'])
def download(current_user):
    print('download')

        

    # try:
    #     
    #     fileTypes = ['application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', 'application/gzip', 'application/pdf', 'application/vnd.ms-excel', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', 'application/zip', 'text/plain']
    #     if 'file' not in request.files:
    #         return jsonify({'error':'no file uploaded'}), 400
    #     file = request.files['file']
    #     if file.mimetype in imageTypes:
    #         file.save(os.path.join(basedir, 'static', f'{current_user.username}', file.filename))
    #         new_file = File(name=file.filename, size=os.path.getsize(f'static/{current_user.username}/{file.filename}'), type=file.mimetype, location=f'static/{current_user.username}/{file.filename}', user_id=uuid.UUID(f'{current_user.id}'))
    #         session.add(new_file)
    #         session.commit()
    #     elif file.mimetype in fileTypes:
    #         file.save(os.path.join(basedir, 'docs', f'{current_user.username}', file.filename))
    #         new_file = File(name=file.filename, size=file.filesize, type=file.mimetype, location=f'docs/{current_user.username}/{file.filename}', user_id=current_user)
    #         session.add(new_file)
    #         session.commit()
    #     else:
    #         return jsonify({'error':'file type not accepted'}), 400
    #     return jsonify('file uploaded successfully'), 201
    # except Exception as ex:
    #     print(ex)
    #     session.rollback()
    #     return jsonify({'error':'error uploading file'}), 500




