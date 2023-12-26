from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL
import pymysql


mysql = MySQL()

def create_app():
    app = Flask(__name__)

    # Configure MySQL database
    app.config['MYSQL_HOST'] = 'localhost'
    app.config['MYSQL_USER'] = 'admin123'
    app.config['MYSQL_PASSWORD'] = '1234'
    app.config['MYSQL_DB'] = 'users'
    app.config['MYSQL_DB1'] = 'users_problems'
    app.config['MYSQL_CURSORCLASS'] = 'DictCursor'  # To receive results as dictionaries

    # Initialize MySQL
    mysql.init_app(app)

    # Rest of your routes...
    
    @app.route('/')
    def index():
        return render_template('index.html')
    
    @app.route('/about.html')
    def about():
        return render_template('about.html')

    @app.route('/contact.html')
    def contact():
        return render_template('contact.html')

    @app.route('/services.html')
    def services():
        return render_template('services.html')
    
    @app.route('/consulting.html')
    def consulting():
        return render_template('consulting.html')
    
    @app.route('/networking.html')
    def networking():
        return render_template('networking.html')
    
    @app.route('/learn.html')
    def learn():
        return render_template('learn.html')
    
    @app.route('/financial.html')
    def financial():
        return render_template('financial.html')
    
    @app.route('/marketing.html')
    def marketing():
        return render_template('marketing.html')


    @app.route('/signup.html', methods=['GET', 'POST'])
    def signup():
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']

            # Insert the user into the database
            conn = mysql.connection
            cursor = conn.cursor()
            cursor.execute('INSERT INTO users (username, password) VALUES (%s, %s)', (username, password))
            conn.commit()
            cursor.close()

            # Redirect to a success page or display a success message
            return redirect(url_for('signup_success'))

        return render_template('signup.html')

    # Signup success route
    @app.route('/signup-success')
    def signup_success():
        return 'Signup completed successfully!'

    @app.route('/feedback.html', methods=['GET', 'POST'])
    def feedback():
        if request.method == 'POST':
            name = request.form['name']
            email = request.form['email']
            rating = request.form['rating']
            message = request.form['message']
            
            conn = mysql.connection
            cursor = conn.cursor()
            cursor.execute("INSERT INTO feedback (name, email, rating, message) VALUES (%s, %s, %s, %s)", (name, email, rating, message))
            conn.commit()
            cursor.close()

            return redirect(url_for('feedback_success'))

        return render_template('feedback.html')
       
    @app.route('/feedback-success')
    def feedback_success():
        return 'Feedback completed successfully! Thanks for your feedback!'
    
    def redirect_to_fetch_data():
    # Perform any necessary actions before redirecting, if needed
    # ...

    # Redirect to the fetch_data.php file
        return redirect('http://localhost/fetch_data.php')


    @app.route('/search.html', methods=['GET', 'POST'])
    def search():
        search_query = ""  # Default value

        if request.method == 'POST':
            search_query = request.form['search_query'].strip()  # Remove leading and trailing whitespaces

            if not search_query:
                # If the search query is empty, redirect to the search page or display an error message
                return render_template('search.html', error_message='Please enter a valid search query')

        try:
            cursor = mysql.connection.cursor()

            # Example query to fetch answers based on the search query for two questions
            cursor.execute("""
                SELECT up.id, up.question1, up.answer1_1, up.answer1_2,
                       up.question2, up.answer2_1, up.answer2_2,
                       a.answer_text
                FROM users_problems up
                LEFT JOIN answers a ON up.id = a.question_id
                WHERE up.question1 LIKE %s OR up.question2 LIKE %s
            """, ('%' + search_query + '%', '%' + search_query + '%'))

            results = cursor.fetchall()
            cursor.close()

            if results:
                # Organize results into a dictionary based on question IDs
                search_results = {}
                for row in results:
                    question_id = row['id']
                    question = row['question1'] if search_query in row['question1'] else row['question2']
                    answer_text = row['answer_text']
                    if question_id not in search_results:
                        search_results[question_id] = {'question': question, 'answers': [answer_text] if answer_text else []}
                    else:
                        search_results[question_id]['answers'].append(answer_text)

                # Render the search results page with the retrieved answers
                return render_template('search.html', search_query=search_query, search_results=search_results)
            else:
                return render_template('search.html', search_query=search_query, search_results=None)

        except Exception as e:
            # Print or log the error for debugging
            print(f"Error: {e}")

            return render_template('search.html', search_query=search_query)

    return app

# Create the app using the factory function
app = create_app()

if __name__ == '__main__':
    # Run the app in debug mode
    app.run(debug=True)