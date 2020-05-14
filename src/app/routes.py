from src.app import ns, kb
from flask_restplus import Resource, fields


problem_description_model = ns.model('ProblemDescription', {'problemDescription': fields.String})
recommendation_model = ns.model('Recommendation', {'recommendation': fields.String})
feedback_model = ns.model(
    'Feedback',
    {
        'problemDescription': fields.String,
        'recommendation': fields.String,
        'didHelp': fields.Boolean
    }
)

complement_input_model = ns.model(
    'ProblemRecommendation',
    {
        'problemResume': fields.String,
        'recommendation': fields.String
    }
)


@ns.route('/GetRecommendations')
class GetRecommendation(Resource):
    @ns.doc(body=problem_description_model, required=True)
    @ns.response(200, 'Success', recommendation_model)
    @ns.response(400, 'Error', None)
    def post(self):
        if len(ns.payload) == 0:
            return 'Request is not valid, model wth problemDescription field must be passed', 400

        if 'problemDescription' not in ns.payload or len(ns.payload) > 1:
            return 'Request is not valid, input model must have only one field - problemDescription', 400

        if len(ns.payload['problemDescription']) == 0:
            return 'Request is not valid, problem description must not be empty', 400

        recommendations = kb.infer(ns.payload['problemDescription'])
        return [{'recommendation': r[2]} for r in recommendations]


@ns.route('/LeaveFeedback')
class LeaveFeedback(Resource):
    @ns.doc(body=feedback_model, required=True)
    @ns.response(204, 'Success', None)
    @ns.response(400, 'Error', None)
    def post(self):
        data = ns.payload

        if len(data) == 0:
            return 'Request is not valid, model with problemDescription, ' \
                   'recommendation and didHelp fields must be passed', 400

        if 'problemDescription' not in data or 'recommendation' not in data \
                or 'didHelp' not in data or len(data) > 3:
            return 'Request is not valid, input model must have problemDescription, ' \
                   'recommendation and didHelp fields', 400

        if len(data['problemDescription']) == 0 or len(data['recommendation']) == 0:
            return 'Request is not valid, fields must not be empty', 400

        if not isinstance(data['didHelp'], bool):
            return 'Request is not valid, didHelp must be a boolean flag', 400

        status = kb.rate_recommendation(
            data['problemDescription'],
            data['recommendation'],
            data['didHelp']
        )

        if status == 1:
            return 'Specified recommendation does not exist', 400
        else:
            return '', 204


@ns.route('/AddRecommendation')
class AddRecommendation(Resource):
    @ns.doc(body=recommendation_model, required=True)
    @ns.response(204, 'Success', None)
    @ns.response(400, 'Error', None)
    def post(self):
        if len(ns.payload) == 0:
            return 'Request is not valid, model wth recommendation field must be passed', 400

        if 'recommendation' not in ns.payload or len(ns.payload) > 1:
            return 'Request is not valid, input model must have only one field - recommendation', 400

        if len(ns.payload['recommendation']) == 0:
            return 'Request is not valid, recommendation must not be empty', 400

        status = kb.add_recommendation(ns.payload['recommendation'])

        if status == 1:
            return 'Recommendation already exists', 400
        else:
            return '', 204
