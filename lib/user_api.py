from werkzeug.wrappers import Response
from werkzeug.exceptions import BadRequest, NotAcceptable, MethodNotAllowed, NotFound
from user import User
from json import dumps
import logging
logging.basicConfig(level=logging.DEBUG)


class UserApi(object):

    @staticmethod
    def query(req):
        cars = [dict(car) for car in User.query()]
        result = dumps(cars)
        # logging.info(cars)
        if req.headers['Accept'] != 'application/json':
            raise NotAcceptable()


        return Response(result,
        mimetype='application/json',
        status=200,
        )

    @staticmethod
    def create(req):
        form_data = {key: req.form[key] for key in req.form}

        if not form_data['brand']:
            raise BadRequest('Brand is requried')

        car = User.create(form_data)

        if req.headers['Accept'] != 'application/json':
            raise NotAcceptable()

        result = dumps(dict(car))
        logging.info(result)

        return Response(result,
            mimetype='application/json',
            status=201,
        )

        


    @staticmethod
    def update(req):
        form_data = {key: req.form[key] for key in req.form}
        logging.info(req.params['id'])
        car = User.update(req.params['id'], form_data)


        if not car:
            raise NotFound('car not found')

        if req.headers['Accept'] != 'application/json':
            raise NotAcceptable()

        result = dumps(dict(car))

        return Response(result,
            mimetype='application/json',
            status=200,
        )

    @staticmethod
    def search(req):
        form_data = {key: req.form[key] for key in req.form}
        logging.info(form_data)
        cars = [dict(car) for car in User.search(form_data)]
        # logging.info(cars)
        if not cars:
            raise NotFound('car not found')

        if req.headers['Accept'] != 'application/json':
            raise NotAcceptable()

        result = dumps(cars)

        return Response(result,
            mimetype='application/json',
            status=200,
        )

    @staticmethod
    def remove(req):
        logging.info(req.params['id'])
        car = User.remove(req.params['id'])

        if not car:
            raise NotFound('car not found')

        if req.headers['Accept'] != 'application/json':
            raise NotAcceptable()

        result = dumps(dict(car))

        return Response(result,
            mimetype='application/json',
            status=200,
        )

    @staticmethod
    def findById(req):
        car = User.find_by_id(req.params['id'])
    
        if not car:
            raise NotFound('Car not found')

        if req.headers['Accept'] != 'application/json':
            raise NotAcceptable()

        result = dumps(dict(car))

        return Response(result,
            mimetype='application/json',
            status=200,
        )


