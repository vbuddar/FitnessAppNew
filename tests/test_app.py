import unittest
from application import app, mongo
from flask import session

class FlaskAppTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_home_redirection(self):
        response = self.app.get("/home", follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Login", response.data)

    def test_login_page_loads(self):
        response = self.app.get("/login")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Login", response.data)

    def test_successful_login(self):
        with self.app:
            response = self.app.post("/login", data={"email": "test@test.com", "password": "password"}, follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn("email", session)

    def test_unsuccessful_login(self):
        response = self.app.post("/login", data={"email": "wrong@test.com", "password": "wrongpass"})
        self.assertIn(b"Login Unsuccessful", response.data)

    def test_logout(self):
        with self.app:
            self.app.post("/login", data={"email": "test@test.com", "password": "password"})
            response = self.app.get("/logout", follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertNotIn("email", session)

    def test_register_page_loads(self):
        response = self.app.get("/register")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Register", response.data)

    def test_successful_registration(self):
        response = self.app.post("/register", data={
            "username": "newuser",
            "email": "new@test.com",
            "password": "password",
            "user_type": "student",
        }, follow_redirects=True)
        self.assertIn(b"Account created", response.data)

    def test_duplicate_registration(self):
        response = self.app.post("/register", data={"email": "test@test.com", "password": "password"})
        self.assertIn(b"Email already exists", response.data)

    def test_dashboard_redirects(self):
        response = self.app.get("/dashboard", follow_redirects=True)
        self.assertIn(b"Login", response.data)

    def test_calories_page_loads(self):
        with self.app:
            self.app.post("/login", data={"email": "test@test.com", "password": "password"})
            response = self.app.get("/calories")
            self.assertEqual(response.status_code, 200)

    def test_update_calories(self):
        with self.app:
            self.app.post("/login", data={"email": "test@test.com", "password": "password"})
            response = self.app.post("/calories", data={"food": "Apple (100)", "burnout": "50"}, follow_redirects=True)
            self.assertIn(b"Successfully updated", response.data)

    def test_progress_monitor_page_loads(self):
        with self.app:
            self.app.post("/login", data={"email": "test@test.com", "password": "password"})
            response = self.app.get("/progress_monitor")
            self.assertEqual(response.status_code, 200)

    def test_submit_progress(self):
        with self.app:
            self.app.post("/login", data={"email": "test@test.com", "password": "password"})
            response = self.app.post("/progress_monitor", data={
                "current_weight": "70",
                "goal_weight": "65",
                "waist": "30",
                "hips": "35",
                "chest": "40",
                "notes": "Feeling good!"
            }, follow_redirects=True)
            self.assertIn(b"Progress successfully saved", response.data)

    def test_progress_history_redirect(self):
        response = self.app.get("/progress_history", follow_redirects=True)
        self.assertIn(b"Login", response.data)

    def test_recommend_workout_page_loads(self):
        response = self.app.get("/recommend_workout")
        self.assertEqual(response.status_code, 200)

    def test_beginner_workout_recommendation(self):
        response = self.app.post("/recommend_workout", data={"selectedLevel": "Beginner"}, follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_advanced_workout_recommendation(self):
        response = self.app.post("/recommend_workout", data={"selectedLevel": "Advanced"}, follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_water_page_loads(self):
        with self.app:
            self.app.post("/login", data={"email": "test@test.com", "password": "password"})
            response = self.app.get("/water")
            self.assertEqual(response.status_code, 200)

    def test_add_water_intake(self):
        with self.app:
            self.app.post("/login", data={"email": "test@test.com", "password": "password"})
            response = self.app.post("/water", data={"intake": "250"}, follow_redirects=True)
            self.assertIn(b"Total Intake", response.data)

    def test_clear_water_intake(self):
        with self.app:
            self.app.post("/login", data={"email": "test@test.com", "password": "password"})
            response = self.app.post("/clear-intake", follow_redirects=True)
            self.assertIn(b"Total Intake: 0", response.data)

    def test_submit_review(self):
        with self.app:
            self.app.post("/login", data={"email": "test@test.com", "password": "password"})
            response = self.app.post("/submit_review", data={"name": "John", "review": "Great coach!"}, follow_redirects=True)
            self.assertIn(b"Review submitted successfully", response.data)

    def test_recommend_exercises_redirect(self):
        response = self.app.get("/recommend_exercises", follow_redirects=True)
        self.assertIn(b"Login", response.data)

    def test_friends_page_loads(self):
        with self.app:
            self.app.post("/login", data={"email": "test@test.com", "password": "password"})
            response = self.app.get("/community")
            self.assertEqual(response.status_code, 200)

    def test_send_friend_request(self):
        with self.app:
            self.app.post("/login", data={"email": "test@test.com", "password": "password"})
            response = self.app.post("/ajaxsendrequest", data={"receiver": "friend@test.com"}, follow_redirects=True)
            self.assertIn(b"Request sent", response.data)

    def test_cancel_friend_request(self):
        with self.app:
            self.app.post("/login", data={"email": "test@test.com", "password": "password"})
            response = self.app.post("/ajaxcancelrequest", data={"receiver": "friend@test.com"}, follow_redirects=True)
            self.assertIn(b"Request cancelled", response.data)

    def test_approve_friend_request(self):
        with self.app:
            self.app.post("/login", data={"email": "test@test.com", "password": "password"})
            response = self.app.post("/ajaxapproverequest", data={"receiver": "friend@test.com"}, follow_redirects=True)
            self.assertIn(b"Request approved", response.data)

    def test_trending_recipes_endpoint(self):
        response = self.app.get("/trending_recipes")
        self.assertEqual(response.status_code, 200)

    def test_recipe_suggestions_page_loads(self):
        response = self.app.get("/recipes_page")
        self.assertEqual(response.status_code, 200)

    def test_recommend_by_ingredients(self):
        response = self.app.get("/recommend_by_ingredients?recipe_name=Grilled Chicken Salad")
        self.assertEqual(response.status_code, 200)

if __name__ == "__main__":
    unittest.main()
