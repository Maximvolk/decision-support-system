from src.app.search_engine.search_engine import SearchEngine
from src.app.repository.repository import Repository


class KnowledgeBase:
    def __init__(self, repository, search_engine, config):
        self.repository: Repository = repository
        self.search_engine: SearchEngine = search_engine
        self.config = config

        # self.init_storage()

    def init_storage(self):
        if self.repository.is_db_empty():
            self.repository.fill_storage_from_file(self.config.fill_data_script_path)

        existing_problems = self.repository.get_all_problems()
        self.search_engine.reindex(self.config.db_name, existing_problems)

    def infer(self, problem_description):
        recommendations = []

        # Get most relevant (most similar to input) problems
        similar_problems_id = self.search_engine.search(self.repository.db_name, problem_description)

        # Try to get recommendations suitable for the most similar problems as possible
        for problem_id in similar_problems_id:
            _recommendations = self.repository.get_recommendations_for_problem(problem_id)
            recommendations.extend(_recommendations)

            if len(recommendations) >= self.config.n_recommendations:
                break

        # Remove duplicates
        used_recommendations_ids = []
        _recommendations = []

        for recommendation in recommendations:
            if recommendation[1] not in used_recommendations_ids:
                used_recommendations_ids.append(recommendation[1])
                _recommendations.append(recommendation)

        recommendations = _recommendations

        # Complement with random recommendations if those retrieved is not enough
        if len(recommendations) < self.config.n_recommendations:
            n = self.config.n_recommendations - len(recommendations)
            _recommendations = self.repository.get_n_random_recommendations(n, used_recommendations_ids)
            recommendations.extend(_recommendations)

        # Limit recommendations amount prior to return
        return recommendations[:self.config.n_recommendations]

    def rate_recommendation(self, problem, recommendation, did_help):
        problems_recommendations_map = self.infer(problem)
        problem_id, recommendation_id = None, None

        for item in problems_recommendations_map:
            if item[2] == recommendation:
                problem_id, recommendation_id = item[0], item[1]

        if recommendation_id is None or problem_id is None:
            return 1

        rating = self.repository.get_problem_recommendation_rating(problem_id, recommendation_id)

        if rating:
            new_rating = rating + 1 if did_help else rating - 1

            if new_rating > 0:
                self.repository.update_problem_recommendation_rating(
                    problem_id, recommendation_id, new_rating)

        elif not rating and did_help:
            self.repository.add_problem_recommendation_rating(problem_id, recommendation_id, 1)

    def add_recommendation(self, recommendation):
        return self.repository.add_recommendation(recommendation)
