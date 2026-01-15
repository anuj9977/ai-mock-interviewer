class InterviewState:
    def __init__(self, role=None, difficulty=None):
        # User choices
        self.role = role
        self.difficulty = difficulty

        # Interview tracking
        self.questions_asked = []
        self.answers_given = []

        # Depth control
        self.depth = "basic"   # basic | intermediate | deep

        # Scoring
        self.score = 0

        # Realism controls (PHASE 1)
        self.personality = "neutral"   # neutral | strict | pressure
        self.max_questions = 6
        self.current_question_count = 0

    def add_turn(self, question, answer):
        """Store Q&A and increment interview progress"""
        self.questions_asked.append(question)
        self.answers_given.append(answer)
        self.current_question_count += 1

    def update_depth(self, new_depth):
        self.depth = new_depth

    def update_score(self, points):
        self.score += points

    def history(self):
        """Return full interview transcript"""
        return list(zip(self.questions_asked, self.answers_given))

    def is_interview_complete(self):
        """Check if interview should end"""
        return self.current_question_count >= self.max_questions
