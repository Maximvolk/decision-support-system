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
    def post(self):
        recommendations = kb.infer(ns.payload['problemDescription'])
        return [{'recommendation': r} for r in recommendations]


@ns.route('/LeaveFeedback')
class LeaveFeedback(Resource):
    @ns.doc(body=feedback_model, required=True)
    @ns.response(204, 'Success', None)
    def post(self):
        data = ns.payload
        kb.rate_recommendation(
            data['problemDescription'],
            data['recommendation'],
            data['didHelp'])

        return '', 204


# @ns.route('/AddProblem')
# class AddProblem(Resource):
#     @ns.doc(body=problem_description_model, required=True)
#     @ns.response(204, 'Success', None)
#     def post(self):
#         kb.add_problem(ns.payload['problemDescription'])
#         return '', 204


@ns.route('/AddRecommendation')
class AddRecommendation(Resource):
    @ns.doc(body=recommendation_model, required=True)
    @ns.response(204, 'Success', None)
    def post(self):
        kb.add_recommendation(ns.payload['recommendation'])
        return '', 204
