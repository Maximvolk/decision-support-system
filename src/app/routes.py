from src.app import ns, kb
from flask_restplus import Resource, fields


problem_description_model = ns.model('ProblemDescription', {'problemDescription': fields.String})
recommendation_model = ns.model('Recommendation', {'recommendation': fields.String})

complement_input_model = ns.model(
    'ProblemRecommendation',
    {
        'problemResume': fields.String,
        'recommendation': fields.String
    }
)


@ns.route('/GetRecommendation')
class GetRecommendation(Resource):
    @ns.doc(body=problem_description_model, required=True)
    @ns.response(200, 'Success', recommendation_model)
    def post(self):
        recommendation = kb.infer(ns.payload['problemDescription'])
        return {'recommendation': recommendation}


@ns.route('/ComplementKnowledgeBase')
class ComplementKnowledgeBase(Resource):
    @ns.doc(body=complement_input_model, required=True)
    @ns.response(204, 'Success', None)
    def post(self):
        data = ns.payload
        kb.complement(data['problemResume'], data['recommendation'])

        return '', 204
