import sqlite3
from contextlib import closing


# Knowledge base mock. Here will be decision model
class KnowledgeBase:
    def __init__(self):
        self.default_recommendation = 'Try to Google it'
        self.data = {
            'permission denied': 'Try with "sudo" or edit file permissions',
            'No such file or directory': 'Check file exists and its name',
            'unmet dependencies': 'Check package dependencies and install them first',
            'broken packages.': 'Check package dependencies or try to reinstall package',
        }

        self.db_name = 'test.db'
        conn = sqlite3.connect(self.db_name)
        self.create_db(conn)

    @staticmethod
    def create_db(conn):
        cursor = conn.cursor()
        cursor.execute(
            'CREATE TABLE IF NOT EXISTS problem ('
            '   problem_id INTEGER PRIMARY KEY,'
            '   description TEXT NOT NULL)'
        )
        cursor.execute(
            'CREATE TABLE IF NOT EXISTS recommendation ('
            '   recommendation_id INTEGER PRIMARY KEY,'
            '   recommendation TEXT NOT NULL)'
        )
        cursor.execute(
            'CREATE TABLE IF NOT EXISTS problem_recommendation ('
            '   problem_id INTEGER,'
            '   recommendation_id INTEGER,'
            '   rating INTEGER NOT NULL DEFAULT 0,'
            '   PRIMARY KEY (problem_id, recommendation_id),'
            '   FOREIGN KEY (problem_id)'
            '       REFERENCES problem (problem_id)'
            '           ON DELETE CASCADE ON UPDATE CASCADE'
            '   FOREIGN KEY (recommendation_id)'
            '       REFERENCES recommendation (recommendation_id)'
            '           ON DELETE CASCADE ON UPDATE CASCADE)'
        )
        cursor.close()

    def infer(self, problem_description):
        with sqlite3.connect(self.db_name) as conn:
            with closing(conn.cursor()) as cursor:
                # Get problem id or add it to db
                get_problem_query = 'SELECT problem_id FROM problem WHERE description = ?'
                problem = cursor.execute(get_problem_query, [problem_description]).fetchone()

                if problem is None:
                    cursor.execute('INSERT INTO problem VALUES (NULL, ?)', [problem_description])
                    conn.commit()
                    problem_id = cursor.lastrowid
                else:
                    problem_id = problem[0]

                # Retrieve list of recommendations with rating for specific problem
                query = f'SELECT recommendation.recommendation_id, recommendation, rating FROM problem' \
                        f'  INNER JOIN problem_recommendation' \
                        f'      ON problem.problem_id = problem_recommendation.problem_id' \
                        f'  INNER JOIN recommendation' \
                        f'      ON problem_recommendation.recommendation_id = recommendation.recommendation_id' \
                        f' WHERE problem.problem_id = {problem_id}'
                recommendations = cursor.execute(query).fetchall()

                # Extend result list with random recommendations if it is too small
                if len(recommendations) < 5:
                    amount = 5 - len(recommendations)

                    if amount < 5:
                        # Ignore already selected recommendations to avoid duplicates
                        ignore = ', '.join([str(item[0]) for item in recommendations])
                        query = f'SELECT * FROM recommendation WHERE recommendation_id IN' \
                                f'   (SELECT recommendation_id FROM recommendation' \
                                f'      WHERE recommendation_id NOT IN ({ignore})' \
                                f'      ORDER BY RANDOM() LIMIT {amount})'
                    else:
                        query = f'SELECT * FROM recommendation WHERE recommendation_id IN' \
                                f'   (SELECT recommendation_id FROM recommendation' \
                                f'      ORDER BY RANDOM() LIMIT {amount})'

                    random_recommendations = cursor.execute(query).fetchall()
                    random_recommendations = [tuple([0, item[1], 1]) for item in random_recommendations]

                    recommendations.extend(random_recommendations)

                # Sort by rating descending
                recommendations.sort(key=lambda item: item[2], reverse=True)

        return [r[1] for r in recommendations]

    def rate_recommendation(self, problem, recommendation, did_help):
        with sqlite3.connect(self.db_name) as conn:
            with closing(conn.cursor()) as cursor:
                # Get problem id
                query = f'SELECT problem_id FROM problem WHERE description = ?'
                problem_id = cursor.execute(query, [problem]).fetchone()

                if problem_id is None:
                    return None
                else:
                    problem_id = problem_id[0]

                # Get recommendation id
                query = f'SELECT recommendation_id FROM recommendation WHERE recommendation = ?'
                recommendation_id = cursor.execute(query, [recommendation]).fetchone()

                if recommendation_id is None:
                    return None
                else:
                    recommendation_id = recommendation_id[0]

                # Increment existing rating or add new
                query = f'SELECT rating FROM problem_recommendation' \
                        f'  WHERE problem_id = {problem_id} AND recommendation_id = {recommendation_id}'
                existing_rating = cursor.execute(query).fetchone()

                if existing_rating is None and did_help:
                    query = f'INSERT INTO problem_recommendation VALUES' \
                            f'  ({problem_id}, {recommendation_id}, 1)'
                    cursor.execute(query)
                else:
                    delta = 1 if did_help else -1
                    query = f'UPDATE problem_recommendation SET rating = {existing_rating[0] + delta}' \
                            f'  WHERE problem_id = {problem_id} AND recommendation_id = {recommendation_id}'
                    cursor.execute(query)

                conn.commit()

    def add_problem(self, problem):
        with sqlite3.connect(self.db_name) as conn:
            with closing(conn.cursor()) as cursor:
                cursor.execute('INSERT INTO problem VALUES (NULL, ?)', [problem])

            conn.commit()

    def add_recommendation(self, recommendation):
        with sqlite3.connect(self.db_name) as conn:
            with closing(conn.cursor()) as cursor:
                cursor.execute('INSERT INTO recommendation VALUES (NULL, ?)', [recommendation])

            conn.commit()
